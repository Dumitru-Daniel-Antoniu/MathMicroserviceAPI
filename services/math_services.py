import math

def power(base: int, exponent: int) -> float:
    """Calculate the power of a number."""
    if base > 100 or exponent > 100:
        raise ValueError("Numbers must be <= 100")
    return math.pow(base, exponent)


def sqrt(n: int) -> float:
    """Calculate the square root of a number."""
    if n < 0:
        raise ValueError("Number must be positive")
    if n >= 100000:
        raise ValueError("Number must be < 100000")
    return math.sqrt(n)


def logarithm(n: int, base: int = 10) -> float:
    """Calculate the logarithm of a number with a specified base."""
    if n <= 0:
        raise ValueError("Number must be > 0")
    if base <= 1:
        raise ValueError("Base must be > 1")
    if n > 10000 or base > 10000:
        raise ValueError("Numbers must be <= 10000")
    return math.log(n, base)


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Number must be positive")
    if n > 100:
        raise ValueError("Number must be <= 100")
    return math.factorial(n)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
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
