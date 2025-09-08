#import pytest
from app.calculator import add, subtract



def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2



import os

def test_env_variable():
    env = os.getenv("ENV_NAME")
    assert env == "3.11"
