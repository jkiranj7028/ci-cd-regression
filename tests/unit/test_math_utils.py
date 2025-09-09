import pytest
from app.math_utils import add_numbers, divide
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.math_utils import add_numbers, divide

@pytest.mark.smoke
def test_add_numbers_basic():
    assert add_numbers([1, 2, 3]) == 6.0

def test_add_numbers_handles_strings():
    assert add_numbers(["1", "2.5", 3]) == 6.5

def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_float():
    assert divide(7, 2) == 3.5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
