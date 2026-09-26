from src.progo import progo_1d
best_f, best_x = progo_1d(
    N=200,
    x0=2.0,
    burn_in=200,
    T=5,
    theta=20.0
)

print("Best_x:", best_x)
print("Best_f:", best_f)