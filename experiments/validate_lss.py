from src.lss import lss_progo_1d

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.cos(x**2) + x/5 + 1

def theoretical_mk(x_grid, k):

    unnormalized = np.exp(-k * f(x_grid))

    Z = np.trapezoid(unnormalized, x_grid)

    mk = unnormalized / Z

    return mk

x_grid = np.linspace(0, 5, 1000)

for k in [1, 3, 9]:

    # Generate samples using LSS
    samples = lss_progo_1d(
        f=f,
        N=2000,
        x0=2.0,
        burn_in=2000,
        k=k,
        theta=20.0
    )

    # Calculate theoretical m_k(x)
    mk = theoretical_mk(x_grid, k)

    # Plot both
    plt.figure(figsize=(8, 5))

    plt.hist(
        samples,
        bins=40,
        density=True,
        alpha=0.6,
        label="LSS samples"
    )

    plt.plot(
        x_grid,
        mk,
        linewidth=2,
        label="Theoretical m_k(x)"
    )

    plt.xlabel("x")
    plt.ylabel("Density")
    plt.title(f"k = {k}")
    plt.legend()

    plt.show()