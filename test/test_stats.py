import pytest 

def test_get_total_stats(client, session):
  resp = client.get("/api/stats/totals")
  assert resp.text == "{\"goog_total\":0,\"marathons_finished\":0,\"marathons_total\":0,\"sprints_finished\":0,\"sprints_total\":0,\"user_finished_marathons\":0,\"user_finished_runs\":0,\"user_marathons\":0,\"user_runs\":0,\"users_total\":1}\n"

def test_get_daily_stats(client, session):
  resp = client.get("/api/stats/daily")
  assert resp.status_code == 200
