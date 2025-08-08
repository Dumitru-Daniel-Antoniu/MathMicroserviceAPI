import math

def power(base: float, exponent: float) -> float:
    """Calculate the power of a number."""
    return math.pow(base, exponent)


def sqrt(value: float) -> float:
    """Calculate the square root of a number."""
    if value < 0:
        raise ValueError("Number must be positive")
    return math.sqrt(value)


def logarithm(value: float, base: float = 10) -> float:
    """Calculate the logarithm of a number with a specified base."""
    if value <= 0:
        raise ValueError("Number must be > 0")
    if base <= 1:
        raise ValueError("Base must be > 1")
    return math.log(value, base)


def factorial(value: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if value < 0:
        raise ValueError("Number must be positive")
    return math.factorial(value)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n < 0:
        raise ValueError("Number must be positive")
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
