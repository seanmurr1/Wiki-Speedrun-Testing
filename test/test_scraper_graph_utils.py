import pytest

from wikispeedruns.scraper_graph_utils import batchQuery, getLinks, convertToID, convertToArticleName, numLinksOnArticle, countDigitsInTitle, randomFilter, countWords, getRandomArticle, traceFromStart, convertNamePathToID, articleLinkNumCheck

# Unit test countWords method to meet BC
# Counts number of words in a string
# FOUND FAULT: we do not properly deal with whitespace chars
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
  assert res < 2
  assert not randomFilter(False, 1)


# Unit test countDigitsInTitle for BC
def test_countDigitsInTitle():
  assert countDigitsInTitle("Title with no digits") == 0
  assert countDigitsInTitle("Title with 1 digits") == 1
  assert countDigitsInTitle("123") == 3
  assert countDigitsInTitle("") == 0
  assert countDigitsInTitle("\t  ") == 0






