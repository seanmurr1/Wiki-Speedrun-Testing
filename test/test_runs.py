from pickle import FALSE
from pymysql import DATETIME

import pytest
import json
import datetime


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
  resp = client.post("/api/runs", json={
    "prompt_id": 8
  })
  assert resp.status_code == 200

  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (8,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

#needs work
def test_finish_run(client, cursor, user, session):
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (9)')
  cursor.execute('SELECT run_id FROM sprint_runs')
  print(cursor.fetchall())
  resp = client.post("/api/runs/2", json={
    "run_id": 2,
    "start_time": 1,
    "end_time": 100,
    "path": json.dumps([20, 21])
  })
  #assert resp.status_code == 200
  #print(resp.json)
  cursor.execute("SELECT run_id FROM sprint_runs")
  assert cursor.fetchall()[0] == {'run_id': 2}
  # cursor.execute("SELECT path FROM sprint_runs WHERE run_id = 2")
  # assert cursor.fetchall()[0] == {'path': [20, 21]}
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (9,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")



def test_update_anonymous_sprint_run(client, cursor):
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (10)')
  cursor.execute('SELECT run_id FROM sprint_runs')
  print(cursor.fetchall())
  resp = client.post("/api/runs/update_anonymous", json={
    "user_id": 14
  })
  cursor.execute("SELECT user_id FROM sprint_runs WHERE run_id = 3")

  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (10,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

# not returning any runs
def test_get_all_runs(client, cursor, user, session):
  # create prompts and run
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id) VALUES (11)')
  resp = client.get('/api/runs')
  assert len(resp.json) > 0 
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (11,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")

def test_get_run(client, cursor, user, session): 
  assert 1 == cursor.execute('INSERT INTO sprint_prompts (start, end) VALUES ("A", "B")')
  path = json.dumps([20, 21])
  assert 1 == cursor.execute('INSERT INTO sprint_runs (prompt_id, path, user_id) VALUES (12, %s, 25)', (path,))
  cursor.execute('SELECT * FROM sprint_runs')
  print(cursor.fetchall())
  resp = client.get('/api/runs/5')
  assert resp.status_code == 200
  print(resp.json) 
  assert 1 == cursor.execute("DELETE FROM sprint_runs WHERE prompt_id=%s", (12,))
  assert 1 == cursor.execute("DELETE FROM sprint_prompts")
  assert resp.json["user_id"] == 25
  assert resp.json["run_id"] == 5
  assert resp.json["path"] == [20, 21]

  # delete
  # cursor.execute('SELECT run_id FROM sprint_runs')
  # print(cursor.fetchall())