import numpy as np
import matplotlib.pyplot as plt

def euler_sir(S0, I0, R0, beta, gamma, dt=0.01, Tmax=365.0, stop_when_I_below=None):
    N = S0 + I0 + R0
    steps = int(Tmax / dt) + 1

    t = [0.0]
    S = [float(S0)]
    I = [float(I0)]
    R = [float(R0)]
    peaked = False

    for _ in range(steps - 1):
        s, i, r = S[-1], I[-1], R[-1]
        dS = -beta * s * i / N
        dI =  beta * s * i / N - gamma * i
        dR =  gamma * i

        S.append(s + dt * dS)
        I.append(i + dt * dI)
        R.append(r + dt * dR)
        t.append(t[-1] + dt)

        if len(I) >= 3 and (I[-2] >= I[-3]) and (I[-2] > I[-1]):
            peaked = True
        if stop_when_I_below is not None and peaked and I[-1] < stop_when_I_below:
            break

    return np.array(t), np.array(S), np.array(I), np.array(R)

# Parameters
N = 137000
I0, R0 = 1.0, 0.0
S0 = N - I0 - R0
beta, gamma = 2.0, 1.0
dt = 0.01

# Integrate and plot
t, S, I, R = euler_sir(S0, I0, R0, beta, gamma, dt=dt, Tmax=365.0, stop_when_I_below=1.0)

plt.figure()
plt.plot(t, I)
plt.xlabel("Time")
plt.ylabel("Infected I(t)")
plt.title("SIR via Explicit Euler - New Haven Population")
plt.tight_layout()
plt.show()

def peak_stats(t, I):
    idx = int(np.argmax(I))
    return float(t[idx]), float(I[idx])

t_peak, I_peak = peak_stats(t, I)
print(f"Peak time: {t_peak:.2f}")
print(f"Infected at peak: {I_peak:.0f}")

# beta and gamma ranges nearby
beta_vals  = np.linspace(1.5, 2.5, 40)
gamma_vals = np.linspace(0.5, 1.5, 40)

def sweep_beta_gamma(S0, I0, R0, beta_vals, gamma_vals, dt=0.02, Tmax=365.0):
    time_to_peak = np.full((len(gamma_vals), len(beta_vals)), np.nan)
    infected_at_peak = np.full((len(gamma_vals), len(beta_vals)), np.nan)
    for gi, g in enumerate(gamma_vals):
        for bi, b in enumerate(beta_vals):
            t_, S_, I_, R_ = euler_sir(S0, I0, R0, b, g, dt=dt, Tmax=Tmax, stop_when_I_below=1.0)
            p = int(np.argmax(I_))
            time_to_peak[gi, bi] = float(t_[p])
            infected_at_peak[gi, bi] = float(I_[p])
    return time_to_peak, infected_at_peak

time_to_peak, infected_at_peak = sweep_beta_gamma(S0, I0, R0, beta_vals, gamma_vals, dt=0.02)

plt.figure()
plt.imshow(time_to_peak, origin="lower",
           extent=[beta_vals[0], beta_vals[-1], gamma_vals[0], gamma_vals[-1]],
           aspect="auto")
plt.colorbar(label="Time to peak")
plt.xlabel("beta")
plt.ylabel("gamma")
plt.title("Time to peak vs beta, gamma")
plt.tight_layout()
plt.show()

# vary number of individuals infected at peak
plt.figure()
plt.imshow(infected_at_peak, origin="lower",
           extent=[beta_vals[0], beta_vals[-1], gamma_vals[0], gamma_vals[-1]],
           aspect="auto")
plt.colorbar(label="Peak infected (people)")
plt.xlabel("beta"); plt.ylabel("gamma")
plt.title("Peak infected vs beta, gamma")
plt.tight_layout(); plt.show()

