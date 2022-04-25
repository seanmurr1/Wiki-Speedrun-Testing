import pytest 
from wikispeedruns.marathon import split, getDifficultyScore, genBatch, genPrompts


def test_getDifficultyScore(cursor, client, user, session):
  #res = getDifficultyScore(1, 1, 5)
  print("hi")
  #print(type(res))
  #print(res)
  #for x in res:
  #  print(x)
  #assert False

def test_split_within_bounds_even():
  arr = [1, 2, 3, 4, 5, 6]
  exp = [[1, 2], [3, 4], [5, 6]]
  res = split(arr, 3)
  for i in range(len(exp)):
    assert next(res) == exp[i]

def test_split_within_bounds_odd():
  arr = [1, 2, 3, 4, 5, 6]
  exp = [[1, 2], [3, 4], [5], [6]]
  res = split(arr, 4)
  for i in range(len(exp)):
    assert next(res) == exp[i]   

def test_split_out_bounds():
  arr = [1, 2, 3]
  exp = [[1], [2], [3], [], []]
  res = split(arr, 5)
  for i in range(len(exp)):
    assert next(res) == exp[i] 

def test_split_no_split():
  arr = [1, 2, 3]
  exp = [arr]
  res = split(arr, 1)
  for i in range(len(exp)):
    assert next(res) == exp[i] 
