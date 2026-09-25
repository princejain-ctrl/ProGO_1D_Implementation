import numpy as np

# chosen objective (as used in the paper also in the eg)
def f(x):
    return np.cos(x**2) + x/5 + 1

def theoretical_mk(x_grid, k):

    unnormalized = np.exp(-k * f(x_grid))

    Z = np.trapezoid(unnormalized, x_grid)

    mk = unnormalized / Z

    return mk

np.random.seed(42)

def lss_progo_1d(
        f, N, x0, burn_in, k, theta, seed=None
):

    # print (f(0))
    # print (f(5))
    # print (f(1.756))

    # Initialising the variables (randomly)
    # OVERWRITE
    # N = 2000
    # burn_in = 2000
    # k = 1

    x = x0

    # the thesis had an inconsistency on initialisation of w, i used a different way and will see how it affects the results in the experiment
    w = f(x) + np.random.exponential(scale=1/k)

    # initialising s via the gamma distribution
    # OVERWRITE
    # theta = 20.0

    s= np.random.gamma(
        shape = 2, #as idescribed in the paper
        scale = theta
    )

    l =  np.random.uniform(
        x-s/2,
        x+s/2 
    )

    samples = []
    # Total iterations = burn-in + required samples
    for t in range(N + burn_in):
        # initialising the interval limits [a,b]
        a = l-s/2
        b = l+s/2
        # CLIP THE INTERVAL FOR THE SELECTED DOMAIN
        a = max(a, 0)
        b = min(b, 5)

        # iterating to get slice samples
        while True:
            x_proposed = np.random.uniform(a,b)

            if f(x_proposed) <w:
                break

            if x_proposed < x:
                a = max(a, x_proposed)

            else:
                b = min(b, x_proposed)
        # Accepted sample
        x=x_proposed

        # update w:
        w = f(x) + np.random.exponential(scale=1/k)
        # update s:
        s = np.random.exponential(scale=theta) + 2*abs(l-x)
        # update l:
        l = np.random.uniform(x-s/2, x+s/2)

        if t>= burn_in:
            samples.append(x)

    return np.array(samples)

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

        # increase k
        k = np.e*k
        print(
            f"Iteration {t+1}: "
            f"k={k:.4f}, "
            f"x={x1:.6f}, "
            f"f(x)={f(x1):.6f}"
        )

    return best_f, best_x

# -------------------------------
x_grid = np.linspace(0, 5, 10000)

for k in [0, 1, 3, 9]:

    mk = theoretical_mk(x_grid, k)

    area = np.trapezoid(mk, x_grid)

    print(f"k={k}, integral of m_k =", area)
# --------------------------------
best_f, best_x = progo_1d(
    N=200,
    x0=2.0,
    burn_in=200,
    T=5,
    theta=20.0,
)

print("Best x:", best_x)
print("Best f:", best_f)

# ------------------------
import matplotlib.pyplot as plt


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