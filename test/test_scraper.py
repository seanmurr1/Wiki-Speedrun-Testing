import pytest 

from wikispeedruns.scraper import tracePath, traceBidirectionalPath, Reverse, countWords, randomFilter, checkSports

# Unit test reverse to meet BC
def test_reverse():
  assert Reverse([1, 2, 3]) == [3, 2, 1]
  assert Reverse([1, 2, 3, 7]) == [7, 3, 2, 1]
  assert Reverse([1]) == [1]
  assert Reverse([]) == []
  assert Reverse(["hi", "one"]) == ["one", "hi"]


# Unit test countWords method to meet BC
# Counts number of words in a string
# FOUND FAULT: we do not properly deal with whitespace chars
# This has been changed/refactored in source code
def test_countWords():
  assert countWords("") == 0
  assert countWords("hi test") == 2
  assert countWords("hi-bye") == 2
  assert countWords("This is an automated-message") == 5
  assert countWords("  ") == 0


# Unit test randomFilter method to probe distribution
# TESTING RANDOMENSS HERE
def test_randomFilter():
  numFalse = 0
  numTrue = 0
  percentageTrue = 0.5
  numRuns = 10000
  for i in range(numRuns):
    if randomFilter(True, percentageTrue):
      numTrue += 1
    else:
      numFalse += 1

  res = (abs(numFalse - numTrue) / numRuns) * 100
  assert res < 2.5
  assert not randomFilter(False, 1)


# Unit test checkSports method for BC
def test_checkSports():
  assert checkSports("1991 League ball championship")
  assert not checkSports("1900 League ball championship")
  assert checkSports("2001 season mega")
  assert checkSports("1991 Olympics ball championship")
  assert not checkSports("Tennis 1990 League ball championship")
  assert not checkSports("1990 ")

test_dict1 = {
  0: (1, 0),
  1: (2, 0),
  2: (3, 0),
  3: (4, 0),
  4: (0, 0)
}

test_dict2 = {
  10: (11, 0),
  11: (21, 0),
  3: (7, 0),
  21: (3, 0),
  7: (100, 0),
  100: (4, 0),
  4: (3, 0),
  2: (4, 0)
}

# Unit test tracePath for BC
def test_tracePath():
  assert tracePath(test_dict1, 0, 4) == [4, 3, 2, 1, 0]
  assert tracePath(test_dict1, 2, 4) == [4, 3, 2]
  assert tracePath(test_dict2, 11, 100) == [100, 7, 3, 21, 11]

# Unit test traceBidirectionalPath for BC
def test_traceBidirectionalPath():
  assert traceBidirectionalPath(2, 0, 4, test_dict1, test_dict2) == [0, 4, 3, 2, 4]


# Test get path api endpoint
def test_get_path_api(client, session):
  try:
    resp = client.post("/api/scraper/path", json={
      "start": 1,
      "end": 5
    })
  except RuntimeError: # no path exists here
    pass  

# Database issue with test below:
# def test_gen_prompts_api(client, session):
#   resp = client.post("/api/scraper/gen_prompts", json={
#     "N": 2
#   })

#   print(resp.text)

#   assert False