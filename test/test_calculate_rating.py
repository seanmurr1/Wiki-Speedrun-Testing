import pytest 

from scripts.calculate_rating import _elo_prob, _calculate_seed, _calculate_place, _calculate_desired_seed, _rating_for_seed, _calculate_new_ratings, _update 

# Unit test elo_prob for BC
def test_elo_prob():
  assert round(_elo_prob(2, 1), 6) == 0.501439
  assert round(_elo_prob(10, 21), 6) == 0.484175
  assert round(_elo_prob(0, 5), 6) == 0.492805
  assert round(_elo_prob(0, 0), 6) == 0.5
  assert round(_elo_prob(1, 1), 6) == 0.5
  assert round(_elo_prob(-2, 4), 6) == 0.491366
  assert round(_elo_prob(100, 1), 6) == 0.638738

# Fixture for test data
@pytest.fixture()
def sample_users1():
  users1 = {
    1: {
     "rating": 1500,
      "num_rounds": 0,
      "username": "tzendaya@gmail.com"
    },
    2: {
      "rating": 1000,
      "num_rounds": 0,
      "username": "megatron@gmail.com"
    },
    3: {
      "rating": 1700,
      "num_rounds": 0,
      "username": "wesocc@gmail.com"
    }
  }
  yield users1

# Fixture for test data
@pytest.fixture()
def sample_users2():
  users2 = {
    1: {
     "rating": 100,
      "num_rounds": 0,
      "username": "elon@gmail.com"
    },
    2: {
      "rating": 2000,
      "num_rounds": 2,
      "username": "stad@gmail.com"
    },
    3: {
      "rating": 1650,
      "num_rounds": 1,
      "username": "mutation@gmail.com"
    }
  }
  yield users2

round1 = [1, 2, 3]

# Unit test calculate_seed for BC
def test_calculate_seed(sample_users1):
  _calculate_seed(sample_users1, round1)
  assert round(sample_users1[1]["seed"], 6) == 1.812987
  assert round(sample_users1[2]["seed"], 6) == 2.929288
  assert round(sample_users1[3]["seed"], 6) == 1.257725

# Unit test calculate place for BC
def test_calculate_place(sample_users1):
  _calculate_place(sample_users1, round1)
  assert sample_users1[1]["place"] == 1
  assert sample_users1[2]["place"] == 2
  assert sample_users1[3]["place"] == 3

# Unit test calculate desired seed for BC
def test_calculate_desired_seed(sample_users1, sample_users2):
  _calculate_seed(sample_users1, round1)
  _calculate_place(sample_users1, round1)
  _calculate_desired_seed(sample_users1)
  assert round(sample_users1[1]["desired_seed"], 6) == 1.346472
  assert round(sample_users1[2]["desired_seed"], 6) == 2.420449
  assert round(sample_users1[3]["desired_seed"], 6) == 1.942466

  _calculate_desired_seed(sample_users2)
  assert "desired_seed" not in sample_users2[1]
  assert "desired_seed" not in sample_users2[2]
  assert "desired_seed" not in sample_users2[3]

# Unit test rating for seed for BC
def test_rating_for_seed(sample_users1):
  _calculate_seed(sample_users1, round1)
  _calculate_place(sample_users1, round1)
  _calculate_desired_seed(sample_users1)
  assert _rating_for_seed(sample_users1, round1, 1, sample_users1[1]["desired_seed"]) == 1818
  assert _rating_for_seed(sample_users1, round1, 2, sample_users1[2]["desired_seed"]) == 1433
  assert _rating_for_seed(sample_users1, round1, 3, sample_users1[3]["desired_seed"]) == 1283

# Unit test calculate new ratings for BC
def test_calculate_new_ratings(sample_users1):
  _calculate_seed(sample_users1, round1)
  _calculate_place(sample_users1, round1)
  _calculate_desired_seed(sample_users1)
  _calculate_new_ratings(sample_users1, round1)
  assert sample_users1[1]["rating"] == 1659
  assert sample_users1[2]["rating"] == 1216
  assert sample_users1[3]["rating"] == 1491

# Unit test update for BC
def test_update(sample_users1, sample_users2):
  _update(sample_users1, round1)
  assert sample_users1[1]["num_rounds"] == 1
  assert sample_users1[2]["num_rounds"] == 1
  assert sample_users1[3]["num_rounds"] == 1

  prev = sample_users2.copy()
  _update(sample_users2, [1])
  assert prev == sample_users2

