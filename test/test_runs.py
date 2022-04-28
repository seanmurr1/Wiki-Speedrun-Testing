from pickle import FALSE
from click import prompt
from pymysql import DATETIME

import pytest
import json
import datetime
import time


# PROMPTS = [
#     {
#         "start" : "Johns Hopkins University",
#         "end" : "Baltimore", 
#     },
#     {
#         "start" : "A",
#         "end" : "B", 
#     },
# ]

def test_create_run(client, cursor, user, session):
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  cursor.execute('SELECT prompt_id FROM sprint_prompts')
  prompt_id = cursor.fetchone().get('prompt_id')
  resp = client.post("/api/runs", json={
    "prompt_id": prompt_id
  })
  assert resp.status_code == 200
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

def test_finish_run(client, cursor, user, session):
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  cursor.execute('SELECT prompt_id FROM sprint_prompts')
  prompt_id = cursor.fetchone().get('prompt_id')
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (%s)', (prompt_id))
  cursor.execute('SELECT run_id FROM sprint_runs')
  run_id = cursor.fetchone().get('run_id')
  resp = client.patch("/api/runs/" + str(run_id), json={
    "run_id": run_id,
    "start_time": time.time(),
    "end_time": time.time(),
    "path": json.dumps([20, 21])
  })
  assert resp.status_code == 200
  cursor.execute("SELECT run_id FROM sprint_runs")
  assert cursor.fetchone().get('run_id') == run_id
  cursor.execute("SELECT path FROM sprint_runs WHERE run_id = %s", (run_id,))
  assert cursor.fetchone().get('path') == '"[20, 21]"'
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

def test_update_anonymous_sprint_run(client, cursor):
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  cursor.execute('SELECT prompt_id FROM sprint_prompts')
  prompt_id = cursor.fetchone().get('prompt_id')
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (%s)', (prompt_id,))
  cursor.execute('SELECT run_id FROM sprint_runs')
  run_id = cursor.fetchone().get('run_id')
  resp = client.post("/api/runs/update_anonymous", json={
    # feeling iffy about hard coding this but dont know how to get valid user wo having to add one or import into session which will mess this test up
    "user_id": 14
  })
  cursor.execute("SELECT user_id FROM sprint_runs WHERE run_id = %s", (run_id))
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

def test_get_all_runs(client, cursor, user, session):
  # create prompts and run
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  cursor.execute('SELECT prompt_id FROM sprint_prompts')
  prompt_id = cursor.fetchone().get('prompt_id')
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (%s)', (prompt_id,))
  cursor.execute('SELECT run_id FROM sprint_runs')
  run_id = cursor.fetchone().get('run_id')
  resp = client.get('/api/runs')
  assert len(resp.json) > 0 
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

def test_get_run(client, cursor, user, session): 
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  cursor.execute('SELECT prompt_id FROM sprint_prompts')
  prompt_id = cursor.fetchone().get('prompt_id')
  path = json.dumps([20, 21])
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id, path, user_id) VALUES (%s, %s, %s)', (prompt_id, path, user['user_id']))
  cursor.execute('SELECT run_id FROM sprint_runs')
  run_id = cursor.fetchone().get('run_id')
  resp = client.get('/api/runs/' + str(run_id))
  assert resp.status_code == 200
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (prompt_id,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")
  assert resp.json["user_id"] == user['user_id']
  assert resp.json["run_id"] == run_id
  assert resp.json["path"] == [20, 21]

  # delete
  # cursor.execute('SELECT run_id FROM sprint_runs')
  # print(cursor.fetchall())