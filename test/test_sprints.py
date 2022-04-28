from itsdangerous import json
import pytest
import time

def test_set_prompt_active_time(client, cursor, user, session):
    # create prompts and run
    assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
    cursor.execute('SELECT prompt_id FROM sprint_prompts')
    prompt_id = cursor.fetchone().get('prompt_id')
    # assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (%s)', (prompt_id,))
    # cursor.execute('SELECT run_id FROM sprint_runs')
    # run_id = cursor.fetchone().get('run_id')
    resp = client.patch('/api/sprints/' + str(prompt_id), json={
        "startDate": time.time(),
        "endDate": time.time(), 
        "rated": False
    })
    assert resp.status_code == 200
    #assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
    assert 1 == cursor.execute("DELETE FROM sprint_prompts")
    assert True

# not sure how to define its managed/active/archived or where to access
def test_get_managed_prompts(client, cursor, user, session):
    resp = client.get('/api/sprint/managed')
    print(resp.json)
    assert True

def test_get_active_prompts(client, cursor, user, session):
    assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
    cursor.execute('SELECT prompt_id FROM sprint_prompts')
    prompt_id = cursor.fetchone().get('prompt_id')
    assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (%s)', (prompt_id,))
    cursor.execute('SELECT run_id FROM sprint_runs')
    run_id = cursor.fetchone().get('run_id')
    resp = client.get('/api/sprint/active')
    print(resp.json)
    assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
    assert 1 == cursor.execute("DELETE FROM sprint_prompts")
    assert True

def test_get_archive_prompts(client, cursor, user, session):
    resp = client.get('/api/sprint/archive')
    assert True

def test_get_prompt(client, cursor, user, session):
    assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
    cursor.execute('SELECT prompt_id FROM sprint_prompts')
    prompt_id = cursor.fetchone().get('prompt_id')
    resp = client.get('/api/sprint/' + str(prompt_id))
    print(resp.json)
    assert True

# def test_get_prompt_leaderboard():

# def test_yomama(location,marriage):
#     if location == Baltimore & marriage == False:
#         print("I'm coming for that ass")
#     else: 
#         print("It's okay I have victor's mama")
#     assert False