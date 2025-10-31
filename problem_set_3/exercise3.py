import numpy as np
import matplotlib.pyplot as plt

# define the function and its true derivative
def f(x):
    return x**3

x0 = 3.0
true_deriv = 3 * x0**2  

# step sizes h from 10^-10 to 1 (log spaced)
h = np.logspace(-10, 0, 400)

# approximation of derivative
cal_deriv = (f(x0 + h) - f(x0)) / h

# absolute error 
abs_err = np.abs(cal_deriv - true_deriv)

# find h with minimum error
min_idx = np.nanargmin(abs_err)
h_star = h[min_idx]
err_star = abs_err[min_idx]

# log-log graph
plt.figure(figsize=(7, 5))
plt.loglog(h, abs_err, linewidth=2, color='orange')
plt.xlabel("h", fontsize=12)
plt.ylabel("| [(f(3+h)-f(3))/h ] - f'(3) |", fontsize=12)
plt.title("Absolute error vs step size h (log-log) for f(x)=x³ at x₀=3", fontsize=13)

# highlight the minimum error point
plt.scatter(h_star, err_star, color='black', zorder=5)
plt.annotate(f"min at h≈{h_star:.1e}\nerr≈{err_star:.1e}",
             (h_star, err_star),
             textcoords="offset points", xytext=(15, 10),
             fontsize=10, arrowprops=dict(arrowstyle="->", lw=1))

plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.show()

print(f"Minimum error occurs at h ≈ {h_star:.2e}, error ≈ {err_star:.2e}")
