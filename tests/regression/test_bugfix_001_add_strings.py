import pytest
from app.math_utils import add_numbers

@pytest.mark.regression
def test_bugfix_001_add_numeric_strings():
    """Guard against past bug where strings concatenated instead of added."""
    assert add_numbers(["1", "2"]) == 3.0
