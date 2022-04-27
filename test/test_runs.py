import pytest

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


# def test_create_run(client, cursor, user, session):
#   response = client.post("/api/sprints/", json=PROMPTS[0])
#   print(response.json)
#   resp = client.post("/api/runs", json={
#     "prompt_id": 1
#   })

#   assert resp.status_code() == 200
#   print(resp.text)

#   cursor.execute("SELECT start, end FROM sprint_prompts")
#   assert cursor.fetchone() == PROMPTS[0]
#   cursor.execute("DELETE FROM sprint_prompts")

#   assert False
  

def test_finish_run():
  assert True


def test_update_anonymous_sprint_run():
  assert True


def test_get_all_runs():
  assert True


def test_get_run():  
  assert True
