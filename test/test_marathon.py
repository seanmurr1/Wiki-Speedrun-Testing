import pytest 
from wikispeedruns.marathon import split, getDifficultyScore, genBatch, genPrompts

# Utilize Equivalence Partitioning to BB test split()
# Even bounds
def test_split_within_bounds_even():
  arr = [1, 2, 3, 4, 5, 6]
  exp = [[1, 2], [3, 4], [5, 6]]
  res = split(arr, 3)
  for i in range(len(exp)):
    assert next(res) == exp[i]

# Utilize Equivalence Partitioning to BB test split()
# Odd bounds
def test_split_within_bounds_odd():
  arr = [1, 2, 3, 4, 5, 6]
  exp = [[1, 2], [3, 4], [5], [6]]
  res = split(arr, 4)
  for i in range(len(exp)):
    assert next(res) == exp[i]   

# Utilize Equivalence Partitioning to BB test split()
# More splits than numbers available
def test_split_out_bounds():
  arr = [1, 2, 3]
  exp = [[1], [2], [3], [], []]
  res = split(arr, 5)
  for i in range(len(exp)):
    assert next(res) == exp[i] 

# Utilize Equivalence Partitioning to BB test split()
# No split at all
def test_split_no_split():
  arr = [1, 2, 3]
  exp = [arr]
  res = split(arr, 1)
  for i in range(len(exp)):
    assert next(res) == exp[i] 


def test_create_run(client, cursor, user, session):
  resp = client.post("/api/marathon/runs/", json={
    "path": "",
    "checkpoints": "",
    "prompt_id": 1,
    "time": 0,
    "finished": 10
  })
  assert resp.status_code == 200
  assert 1 == cursor.execute("DELETE FROM marathonruns WHERE prompt_id=%s", (1,))


# def test_update_anonymous_marathon_run(client, cursor):
#   resp = client.post("/api/marathon/runs/", json={
#     "path": "",
#     "checkpoints": "",
#     "prompt_id": 1,
#     "time": 0,
#     "finished": 10
#   })


def test_add_marathon_prompt(client, cursor, user, admin_session):
  resp = client.post("/api/marathon/add/", json={
    "data": {
      "start": 1,
      "startcp": 2,
      "seed": 22,
      "cp": []
    }
  })

  assert resp.status_code == 200
  assert 1 == cursor.execute("DELETE FROM marathonprompts WHERE start=%s", (1,))

def test_delete_prompt(client, cursor, user, admin_session):
  resp = client.post("/api/marathon/add/", json={
    "data": {
      "start": 1,
      "startcp": 2,
      "seed": 22,
      "cp": []
    }
  })
  resp = client.delete("/api/marathon/delete/2")
  assert resp.status_code == 200

def test_get_all_marathon_prompts(client, cursor, user, session):
  resp = client.get("/api/marathon/all")
  assert resp.json == []

def test_get_marathon_prompt(client, cursor, user, admin_session):
  resp = client.post("/api/marathon/add/", json={
    "data": {
      "start": 2,
      "startcp": 2,
      "seed": 2,
      "cp": [2]
    }
  })
  resp = client.get("/api/marathon/prompt/3")
  assert resp.json == {"checkpoints":"[2]","initcheckpoints":"2","prompt_id":3,"public":0,"seed":2,"start":"2"}
  assert 1 == cursor.execute("DELETE FROM marathonprompts WHERE start=%s", (2,))

def test_get_marathon_prompt_leaderboard(client, cursor, user, admin_session):
  resp = client.post("/api/marathon/add/", json={
    "data": {
      "start": 2,
      "startcp": 2,
      "seed": 2,
      "cp": [2]
    }
  })
  resp = client.get("/api/marathon/prompt/3/leaderboard/")
  assert resp.json == []
  assert 1 == cursor.execute("DELETE FROM marathonprompts WHERE start=%s", (2,))

def test_get_marathon_personal_leaderboard(client, cursor, user, admin_session):
  resp = client.get("/api/marathon/echoingsins")
  assert resp.json == []