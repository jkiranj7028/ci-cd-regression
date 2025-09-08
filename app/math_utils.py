from typing import Iterable

def add_numbers(nums: Iterable[float]) -> float:
    """Robust summation that accepts numbers or numeric strings.

    Regression history:
    - Bug #001: strings were concatenated instead of added, e.g. ['1','2'] -> '12'
                 Fixed by always converting to float.
    """
    total = 0.0
    for n in nums:
        total += float(n)  # cast prevents string concatenation bugs
    return total

def divide(a: float, b: float) -> float:
    return a / b
