from pydoc import cli
from pymysql import DATETIME
import pytest

import wikispeedruns

@pytest.fixture
def lobby(cursor, user):
    lobby_id = wikispeedruns.lobbys.create_lobby(user["user_id"])

    cursor.execute(f"SELECT * FROM lobbys WHERE lobby_id={lobby_id}")
    yield cursor.fetchone()

    cursor.execute("DELETE FROM user_lobbys")
    cursor.execute("DELETE FROM lobbys")


def test_create_lobby(cursor, client, session):
    resp = client.post("/api/lobbys", json={
        "name": "testlobby",
        "desc": "lobby for testing",
        "rules": {},
    })

    lobby_id = resp.json["lobby_id"]

    # Assert that we inserted and are now deleting something
    assert 1 == cursor.execute("DELETE FROM user_lobbys WHERE lobby_id=%s", (lobby_id,))
    assert 1 == cursor.execute("DELETE FROM lobbys WHERE lobby_id=%s", (lobby_id,))


def test_join_lobby_anonymous(client, lobby):
    # Join lobby
    lobby_id = lobby["lobby_id"]
    resp = client.post(f"/api/lobbys/{lobby_id}/join", json={
        "name": "anonymous",
        "passcode": lobby["passcode"],
    })
    assert resp.status_code == 200

    # Make sure session is there
    with client.session_transaction() as session:
        # session converts to string it seems?
        session["lobbys"][str(lobby_id)] == "anonymous"

    # Make sure we can get lobby
    resp = client.get(f"/api/lobbys/{lobby_id}")
    assert resp.status_code == 200
    assert resp.json["lobby_id"] == lobby_id

# Test failure conditions of joining lobby
# BB & aim to get BC
def test_join_lobby_failures(client, lobby):
    lobby_id = lobby["lobby_id"]
    resp = client.post(f"/api/lobbys/{None}/join", json={
        "name": "anonymous",
        "passcode": lobby["passcode"],
    })
    assert resp.status_code == 404

    resp = client.post(f"/api/lobbys/{lobby_id}/join", json={
        "name": "anonymous",
        "passcode": "bad_pw",
    })
    assert resp.status_code == 401

    resp = client.post(f"/api/lobbys/{lobby_id}/join", json={
        "passcode": lobby["passcode"],
    })
    assert resp.status_code == 400

    resp = client.post(f"/api/lobbys/123123123/join", json={
        "name": "anonymous",
        "passcode": lobby["passcode"],
    })
    assert resp.status_code == 404


def test_join_lobby_user(client, cursor, session2, lobby):
    lobby_id = lobby["lobby_id"]

    # Join lobby
    resp = client.post(f"/api/lobbys/{lobby_id}/join", json={
        "passcode": lobby["passcode"]
    })
    assert resp.status_code == 200

    # check user shows up in table
    query = "SELECT owner FROM user_lobbys WHERE user_id=%s AND lobby_id=%s"
    cursor.execute(query, (session2["user_id"], lobby_id))
    res = cursor.fetchone()
    assert res is not None and res["owner"] == False

    # Check we have new permissions
    resp = client.get(f"/api/lobbys/{lobby_id}")
    assert resp.status_code == 200
    assert resp.json["lobby_id"] == lobby_id


def test_permissions_anonymous(client, lobby):
    lobby_id = lobby["lobby_id"]

    resp = client.get(f"/api/lobbys/{lobby_id}")
    assert resp.status_code == 401

    resp = client.get(f"/api/lobbys/{lobby_id}/prompts")
    assert resp.status_code == 401


# small note, order of session and lobby matter, else this attempts to delete
# user without deleting from user_lobby
def test_permissions_user(client, session2, lobby):
    lobby_id = lobby["lobby_id"]

    resp = client.get(f"/api/lobbys/{lobby_id}")
    assert resp.status_code == 401

    resp = client.get(f"/api/lobbys/{lobby_id}/prompts")
    assert resp.status_code == 401

    # Join lobby as non owner, make sure prompt endpoints don't work
    resp = client.post(f"/api/lobbys/{lobby_id}/join", json={
        "passcode": lobby["passcode"]
    })

    resp = client.post(f"api/lobbys/{lobby_id}/prompts", json={
        "start": "test",
        "end": "test"
    })
    assert resp.status_code == 401

# Test failure conditions of trying to get a lobby
def test_get_add_prompt_to_lobby(cursor, client, session):
    resp = client.post("/api/lobbys", json={
        "name": "testlobby",
        "desc": "lobby for testing",
        "rules": {},
    })
    lobby_id = resp.json["lobby_id"]
    resp = client.post(f"api/lobbys/{lobby_id}/prompts", json={
        "start": "test",
        "end": "test"
    })
    assert resp.status_code == 200

    # Assert that we inserted and are now deleting something
    assert 1 == cursor.execute("DELETE FROM lobby_prompts WHERE lobby_id=%s", (lobby_id,))
    assert 1 == cursor.execute("DELETE FROM user_lobbys WHERE lobby_id=%s", (lobby_id,))
    assert 1 == cursor.execute("DELETE FROM lobbys WHERE lobby_id=%s", (lobby_id,))

# Test API to get lobby prompts
def test_get_lobby_prompts(cursor, client, session):
    resp = client.post("/api/lobbys", json={
        "name": "testlobby",
        "desc": "lobby for testing",
        "rules": {},
    })
    lobby_id = resp.json["lobby_id"]

    resp = client.get(f"api/lobbys/{lobby_id}/prompts/1")
    assert resp.status_code == 404

    resp = client.post(f"api/lobbys/{lobby_id}/prompts", json={
        "start": "test",
        "end": "test"
    })
    assert resp.status_code == 200

    resp = client.get(f"api/lobbys/{lobby_id}/prompts")
    assert resp.text == "[{\"end\":\"test\",\"prompt_id\":1,\"start\":\"test\"}]\n"

    resp = client.get(f"api/lobbys/{lobby_id}/prompts/1")
    assert resp.text == "{\"end\":\"test\",\"prompt_id\":1,\"start\":\"test\"}\n"

    # Assert that we inserted and are now deleting something
    assert 1 == cursor.execute("DELETE FROM lobby_prompts WHERE lobby_id=%s", (lobby_id,))
    assert 1 == cursor.execute("DELETE FROM user_lobbys WHERE lobby_id=%s", (lobby_id,))
    assert 1 == cursor.execute("DELETE FROM lobbys WHERE lobby_id=%s", (lobby_id,))

import datetime

# # Test API to add prompt run to lobby
# def test_get_lobby_prompts(cursor, client, session):
#     # Create lobby
#     resp = client.post("/api/lobbys", json={
#         "name": "testlobby",
#         "desc": "lobby for testing",
#         "rules": {},
#     })
#     lobby_id = resp.json["lobby_id"]

#     # Create prompt
#     resp = client.post(f"api/lobbys/{lobby_id}/prompts", json={
#         "start": "test",
#         "end": "test"
#     })

#     resp = client.post(f"api/lobbys/{lobby_id}/prompts/1/runs", json={
#         "start_time": 10,
#         "end_time": 100
#     })

#     print(resp.text)

#     # Assert that we inserted and are now deleting something
#     #assert 1 == cursor.execute("DELETE FROM lobby_runs WHERE lobby_id=%s", (lobby_id,))
#     assert 1 == cursor.execute("DELETE FROM lobby_prompts WHERE lobby_id=%s", (lobby_id,))
#     assert 1 == cursor.execute("DELETE FROM user_lobbys WHERE lobby_id=%s", (lobby_id,))
#     assert 1 == cursor.execute("DELETE FROM lobbys WHERE lobby_id=%s", (lobby_id,))
#     assert False



from wikispeedruns.lobbys import _random_passcode

def test_random_passcode():
    for _ in range(1000):
        pw = _random_passcode()
        assert len(pw) == 6
        assert int(pw) >= 0
        assert int(pw) <= 999999