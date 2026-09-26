ProGO 1-D IMPLEMENTATION:

This repository contains a Python implementation of the 1-D ProGO framework described in Xinyu Zhang's PhD thesis.
The current work focuses only on reproducing and understanding the 1-D ProGO formulation, particularly the Latent Slice Sampler (LSS) and the evolution of the nascent-minima distribution as the concentration parameter k increases.

ABOUT PAPER:

ProGO converts an optimization problem: minimize f(x), x ∈ Ω into a sequence of probability distributions
m_k(x) = exp(-k f(x)) PI(x) / Z_k

where PI(x) is a prior and k controls the concentration of the distribution around low values of f(x).
As k increases, m_k places increasing probability mass around global minimizers.
The paper samples from m_k using a Latent Slice Sampler (LSS). ProGO then increases k iteratively and uses the resulting samples to search for the global minimum.
For the 1-D example, the paper uses
f(x) = cos(x²) + x/5 + 1
x ∈ [0,5]
with a uniform prior. The reported global minimum is approximately x ≈ 1.756 f(x) ≈ 0.353

WHAT I IMPLEMENTED:

The implementation is divided into:
src/lss.py
1-D Latent Slice Sampler
src/progo.py
ProGO outer loop
experiments/validate_lss.py
Comparison of LSS samples with the theoretical m_k
experiments/run_progo_1d.py
1-D ProGO optimization experiment

The LSS implementation follows the latent-variable formulation from the paper:
w = f(x) + Exp(k)  together with the slice construction and latent scale/location updates.

The ProGO loop starts with k = 5 and updates k tO e^K after each iteration.

For the current uniform-prior example, candidate samples can be ranked using -k*f(x) because PI(x) is constant and the normalizing constant is common to all samples at a fixed k.

VALIDATION: 

Two main experiments were performed.

LSS distribution validation:

The empirical LSS samples were compared with the numerically normalized theoretical m_k for k = 1, 3, 9 using
N = 2000
burn-in = 2000
x0 = 2
θ = 20
The empirical histograms follow the corresponding theoretical distributions, including their increasing concentration around low values of f(x).

PROGO OPTIMIZATION:

Using
N = 200
burn-in = 200
T = 5
x0 = 2
θ = 20
initial k = 5
the implementation reaches approximately x = 1.756 f(x) = 0.352884 which is consistent with the minimum reported for the 1-D example.

ASSUMPTIONS AND IMPLEMENTATION CHOICES:

The following assumptions are specific to the current 1-D implementation:
-The domaiN is fixed to [0,5], matching the paper's 1-D example.
- The prior PI(x) is uniform on [0,5]. (and therefore, the implementation does not use pi_x function to initialise the distribution since the constant cancels out eventually.)
- θ = 20 is used as in the 1-D experiment.
- x0 = 2 is used as the initial point. (I was not sure whether x0 should be constant for all iterations or should be updated to x1, and the experiment works without updation)
- - N and burn-in are fixed as described above.
- The random seed is fixed to 42 for reproducibility.
- LSS samples are treated as Markov-chain samples; they are not assumed to be independent.
- The current validation is distributional/visual; no formal MCMC convergence or effective-sample-size analysis has been performed.

DIFFERENCES AND INCONSISTENCIES COUNTERED:

- Initialization of w: 
The paper's Algorithm 1 specifies an initial
w^(0) ~ Uniform(0, π(x^(0)))
but later updates w using
w^(t) = f(x^(t)) + Exp(k)
The latter is also consistent with the conditional distribution implied by the latent joint density. The implementation therefore uses w = f(x) + Exp(k) for initialization as well.

- k = 0: 
The theoretical formulation includes k = 0, where
m_0(x) = PI(x)
but the LSS update uses Exp(k), which is not directly defined for rate k = 0. Therefore k = 0 is treated as a theoretical/reference case, not as a normal LSS iteration.

- Domain handling: 
The paper describes the slice construction over the domain. In the current Python implementation, the proposal interval is explicitly clipped to [0,5] because this is the domain of the reproduced 1-D example.

- Normalization: 
Z_k is calculated numerically when plotting the theoretical m_k for validation, but is not calculated during candidate selection. This is unnecessary for ranking samples because Z_k is common to all candidates at a fixed k.

- Log-density: 
Candidate selection uses -k*f(x) instead of directly computing exp(-k f(x)). This gives the same ordering for the uniform prior and is numerically safer for larger k.

- Random seed: 
The seed is set once before the ProGO experiment rather than inside LSS. This allows successive ProGO iterations to use different random draws while keeping the overall experiment reproducible.

5, 13.5914, 36.9453, 100.4277, ...

CURRENT STATUS:

The 1-D LSS and ProGO implementation is working for the thesis example, and the LSS distribution and optimization behaviour have been numerically checked.

The repository is intentionally limited to the 1-D case. Higher-dimensional benchmarks and the other experiments in the thesis have not been reproduced here.
