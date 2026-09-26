import numpy as np
from src.lss import lss_progo_1d

# chosen objective (as used in the paper also in the eg)
def f(x):
    return np.cos(x**2) + x/5 + 1

np.random.seed(42)

# ----------------------------------------------------

def progo_1d(N, x0, burn_in, T, theta):

    k = 5.0

    best_x = None
    best_f = np.inf

    for t in range(T):
        # sample from m_k using LSS
        samples = lss_progo_1d(
            f=f,
            N=N,
            x0=x0,
            burn_in=burn_in,
            k=k,
            theta=theta
        
        )

        x=x0
        # finding sample with max m_k:
        log_density = -k*np.array([f(x) for x in samples])

        best_index = np.argmax(log_density)

        x1 = samples[best_index]

        # now see best objective value"
        if f(x1) < best_f:
            best_f = f(x1)
            best_x = x1

        
        print(
            f"Iteration {t+1}: "
            f"k={k:.4f}, "
            f"x={x1:.6f}, "
            f"f(x)={f(x1):.6f}"
        )
        # increase k
        k = np.e*k

    return best_f, best_x