import pytest

from wikispeedruns.prompt_generator import checkSports

# Unit test checkSports method for BC
def test_checkSports():
  assert checkSports("1991 League ball championship")
  assert not checkSports("1900 League ball championship")
  assert checkSports("2001 season mega")
  assert checkSports("1991 Olympics ball championship")
  assert not checkSports("Tennis 1990 League ball championship")

