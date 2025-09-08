#import pytest
#from app.calculator import add, subtract


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b


def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2
