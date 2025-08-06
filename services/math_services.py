import math
from functools import lru_cache


def power(base: float, exponent: float) -> float:
    """Calculate the power of a number."""
    print("Power is calculated")
    return math.pow(base, exponent)


def sqrt(value: float) -> float:
    """Calculate the square root of a number."""
    print("Square root is calculated")
    if value < 0:
        raise ValueError("Cannot compute square root of negative number")
    return math.sqrt(value)


def logarithm(value: float, base: float = 10) -> float:
    """Calculate the logarithm of a number with a specified base."""
    print("Logarithm is calculated")
    if value <= 0:
        raise ValueError("Logarithm undefined for non-positive values")
    if base <= 1:
        raise ValueError("Base must be greater than 1")
    return math.log(value, base)


def factorial(value: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    print("Factorial is calculated")
    return math.factorial(value)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    print("Fibonacci is calculated")
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
