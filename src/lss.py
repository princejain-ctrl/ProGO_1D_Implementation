import numpy as np

def lss_progo_1d(
        f, N, x0, burn_in, k, theta
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