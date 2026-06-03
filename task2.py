from random import Random

from scipy.integrate import quad


def f(x: float) -> float:
    return x ** 2


def monte_carlo_integral(func, a: float, b: float, samples: int, seed: int = 42) -> float:
    rng = Random(seed)
    total = 0.0

    for _ in range(samples):
        x = rng.uniform(a, b)
        total += func(x)

    average_value = total / samples
    return (b - a) * average_value


def analytical_integral(a: float, b: float) -> float:
    return (b ** 3 - a ** 3) / 3


def main() -> None:
    a = 0.0
    b = 2.0
    samples = 100_000

    monte_carlo_result = monte_carlo_integral(f, a, b, samples)
    quad_result, quad_error = quad(f, a, b)
    analytical_result = analytical_integral(a, b)

    print("Function: f(x) = x^2")
    print(f"Interval: [{a}, {b}]")
    print(f"Samples: {samples}")
    print()
    print(f"Monte Carlo result: {monte_carlo_result:.6f}")
    print(f"SciPy quad result:  {quad_result:.6f}")
    print(f"Analytical result:  {analytical_result:.6f}")
    print(f"quad error:         {quad_error:.12f}")
    print()
    print(f"Monte Carlo absolute error vs quad: {abs(monte_carlo_result - quad_result):.6f}")
    print(f"Monte Carlo absolute error vs analytical: {abs(monte_carlo_result - analytical_result):.6f}")


if __name__ == "__main__":
    main()
