import pytest 


def test_get_username(cursor, client, session):
  username_good = "echoingsins"
  resp = client.get(f"/api/profiles/{username_good}/")
  assert resp.status_code == 200
  resp = client.get(f"/api/profiles/badname/")
  assert resp.status_code == 404

def test_total_stats(cursor, client, session):
  resp = client.get(f"/api/profiles/echoingsins/stats")
  assert resp.json == {'total_prompts': 0, 'total_runs': 0}

# Test get endpoint for streaks for a profile
def test_get_streaks(cursor, client, session):
  resp = client.get(f"/api/profiles/streak")
  assert resp.text == "{\"done_today\":0,\"streak\":0}\n"
  assert resp.status_code == 200


