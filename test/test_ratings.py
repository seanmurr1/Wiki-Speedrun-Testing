import pytest 

# Test API endpoint to get top ratings in database
def test_get_top_ratings(client, session):
  resp = client.get("/api/ratings")
  assert resp.text == "[]\n"