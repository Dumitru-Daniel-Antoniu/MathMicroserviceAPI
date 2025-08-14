"""
Mathematical operation services for FastAPI endpoints.

Implements core mathematical functions with input validation,
including power, square root, logarithm, factorial and Fibonacci calculations.
"""

import math


def power(base: int, exponent: int) -> float:
    """
    Calculate the power of a base raised to an exponent.

    Args:
        base (int): The base number (<= 100).
        exponent (int): The exponent (<= 100).

    Returns:
        float: Result of base ** exponent.

    Raises:
        ValueError: If base or exponent exceeds 100.
    """

    if base > 100 or exponent > 100:
        raise ValueError("Numbers must be <= 100")
    return math.pow(base, exponent)


def sqrt(n: int) -> float:
    """
    Calculate the square root of a number.

    Args:
        n (int): Input number (0 <= n < 100000).

    Returns:
        float: Square root of n.

    Raises:
        ValueError: If n is negative or >= 100000.
    """

    if n < 0:
        raise ValueError("Number must be positive")
    if n >= 100000:
        raise ValueError("Number must be < 100000")
    return math.sqrt(n)


def logarithm(n: int, base: int = 10) -> float:
    """
    Calculate the logarithm of a number with a given base.

    Args:
        n (int): Input number (0 < n <= 10000).
        base (int): Logarithm base (1 < base <= 10000).

    Returns:
        float: Logarithm of n to the given base.

    Raises:
        ValueError: If n <= 0, base <= 1,
                    or values exceed 10000.
    """

    if n <= 0:
        raise ValueError("Number must be > 0")
    if base <= 1:
        raise ValueError("Base must be > 1")
    if n > 10000 or base > 10000:
        raise ValueError("Numbers must be <= 10000")
    return math.log(n, base)


def factorial(n: int) -> int:
    """
    Calculate the factorial of a number.

    Args:
        n (int): Input number (0 <= n <= 100).

    Returns:
        int: Factorial of n.

    Raises:
        ValueError: If n is negative or > 100.
    """

    if n < 0:
        raise ValueError("Number must be positive")
    if n > 100:
        raise ValueError("Number must be <= 100")
    return math.factorial(n)


def fibonacci(n: int) -> int:
    """
    Calculate the n-th Fibonacci number using fast doubling.

    Args:
        n (int): Index of Fibonacci number (0 <= n <= 1000).

    Returns:
        int: n-th Fibonacci number.

    Raises:
        ValueError: If n is negative or > 1000.
    """

    if n < 0:
        raise ValueError("Number must be positive")
    if n > 1000:
        raise ValueError("Number must be <= 1000")

    def fast_fib(k: int):
        if k == 0:
            return (0, 1)
        a, b = fast_fib(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        else:
            return (c, d)
    return fast_fib(n)[0]
