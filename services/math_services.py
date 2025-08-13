import math

def power(base: float, exponent: float) -> float:
    """Calculate the power of a number."""
    if base > 100 or exponent > 100:
        raise ValueError("Numbers must be <= 100")
    return math.pow(base, exponent)


def sqrt(value: float) -> float:
    """Calculate the square root of a number."""
    if value < 0:
        raise ValueError("Number must be positive")
    if value >= 100000:
        raise ValueError("Number must be < 100000")
    return math.sqrt(value)


def logarithm(value: float, base: float = 10) -> float:
    """Calculate the logarithm of a number with a specified base."""
    if value <= 0:
        raise ValueError("Number must be > 0")
    if base <= 1:
        raise ValueError("Base must be > 1")
    if value > 1000 or base > 1000:
        raise ValueError("Numbers must be <= 1000")
    return math.log(value, base)


def factorial(value: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if value < 0:
        raise ValueError("Number must be positive")
    if value > 100:
        raise ValueError("Number must be <= 100")
    return math.factorial(value)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n < 0:
        raise ValueError("Number must be positive")
    if n > 100:
        raise ValueError("Number must be <= 100")
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
