import pytest 

from wikispeedruns.auth.passwords import valid_password, hash_password

# Unit tes valid_password for BC
# Ensure we meet password standards
def test_valid_password():
  assert valid_password("asdfasfd sadf") == None
  assert not valid_password("12345")
  assert not valid_password("hello")
  assert valid_password("supersecretpassword") == None