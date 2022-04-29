from datetime import datetime
import enum
import pytest

from wikispeedruns.prompts import compute_visibility, Prompt

PROMPTS = [
    {
        "start" : "Johns Hopkins University",
        "end" : "Baltimore", 
    },
    {
        "start" : "A",
        "end" : "B", 
    },
]


@pytest.fixture()
def prompt_set(cursor):
    query = "INSERT INTO sprint_prompts (prompt_id, start, end) VALUES (%s, %s, %s);"
    ps = [(i, p["start"], p["end"]) for i, p in enumerate(PROMPTS)]
    cursor.executemany(query, ps)

    yield

    cursor.execute("DELETE FROM sprint_prompts")


def test_create_prompt(client, cursor, admin_session):
    response = client.post("/api/sprints/", json=PROMPTS[0])
    assert response.status_code == 200
    
    cursor.execute("SELECT start, end FROM sprint_prompts")
    assert cursor.fetchone() == PROMPTS[0]
    cursor.execute("DELETE FROM sprint_prompts")



def test_create_no_admin(client, cursor):
    response = client.post("/api/sprints/", json=PROMPTS[0])
    assert response.status_code == 401
    
    cursor.execute("SELECT start, end FROM sprint_prompts")
    assert cursor.fetchone() is None



def test_delete(client, cursor, prompt_set, admin_session):
    # Try deleting id 1, which should be inserted
    id = 1
    response = client.delete(f"/api/sprints/{id}")
    assert response.status_code == 200
    cursor.execute("SELECT start, end FROM sprint_prompts WHERE prompt_id=%s", (id, ))
    assert cursor.fetchone() is None


def test_delete_nonexistent(client, cursor, prompt_set, admin_session):
    # Try deleting id 1, which should be inserted
    id = len(PROMPTS)
    response = client.delete(f"/api/sprints/{id}")
    assert response.status_code == 404


def test_delete_no_admin(client, cursor, prompt_set):
    id = 1
    response = client.delete(f"/api/sprints/{id}")
    assert response.status_code == 401
    cursor.execute("SELECT start, end FROM sprint_prompts WHERE prompt_id=%s", (id, ))
    assert cursor.fetchone() == PROMPTS[id]


prompt1 = {
    "prompt_id": 1,
    "start": "",
    "active_start": datetime.now(),
    "active_end": datetime.now(),

    "used": False,
    "available": True,
    "active": True,
    "played": False
}

prompt2 = {
    "prompt_id": 1,
    "start": "",
    "active_start": None,
    "active_end": None,

    "used": True,
    "available": True,
    "active": True,
    "played": False
}

# Unit test compute_visibility for BC
def test_compute_visibility():
    p1 = compute_visibility(prompt1)
    assert p1["used"]
    assert p1["available"]
    assert not p1["active"]

    p2 = compute_visibility(prompt2)
    assert not p2["used"]
    assert p2["available"]
    assert p2["active"]
    assert not p2["played"]

