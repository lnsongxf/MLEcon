# Copyright 2018 Victor Duarte. All Rights Reserved.
import mlecon as mle
import matplotlib.pyplot as plt
import numpy as np

mle.clear()  # Reset graph
dt = mle.dt  # Symbolic placeholder

# Model Parameters
g = 2.20 / 100 / 4
σ = 0.86 / 100 / np.sqrt(4)
γ = 2.37
b = 0.011
ϕ = .89 ** (1 / 4)
δ = (.93)**(1 / 4)
ρ = -np.log(δ)

# Hyper-parameters
hidden = [10, 10]  # number of units in each hidden layer
Δt = 1e-2          # dt for simulation
mle.set_batch_size(256)

# State space - log dividends and log consumption-surplus ratio
d = mle.state(-2, 2)
s = mle.state(np.log(1e-6), np.log(0.07), sampling='exp_uniform')

# Brownian shock
dZ = mle.brownian_shocks(1)

# Function approximators
j = mle.network([d, s], name='log_VF', hidden=hidden)


# %% ------------Economic Model ----------------------------
S = mle.exp(s)
S_bar = σ * np.sqrt(γ / (1 - ϕ - b / γ))
s_bar = np.log(S_bar)
λ = 1 / S_bar * mle.sqrt(1 - 2 * (s - s_bar)) - 1

# Consumption
D = mle.exp(d)
C = D
c = mle.log(C)

# Marginal Utility and prices
m = -γ * (s + c)
P = mle.exp(j - m)
u = d + m

# Price-dividend ratio
F = P / D

# State dynamics
d.d = g * dt + σ * dZ
s.d = (1 - ϕ) * (s_bar - s) * dt + λ * σ * dZ

HJB = mle.exp(u - j) - ρ + (j.drift() + 0.5 * j.var())  # (log) HJB residuals
T = j + mle.log(1 + Δt * HJB)                       # bellman target

# Policy evaluation
policy_evaluation = mle.fit(j, T)

# %% -------------------------------------------------------------
# Launch graph
mle.launch()


# %% -------------- test function ------------------------------------
def test():
    s_ = np.log(np.linspace(1e-5, 0.07, mle.get_batch_size()))
    feed_dict = {d: 0, s: s_}
    xx, yy = mle.run([S, F], feed_dict)
    plt.plot(xx, yy)
    plt.show()
    plt.pause(1e-6)


# %% --------------- main iteration -------------------------------------
program = {policy_evaluation: 1, test: 1000}
mle.iterate(program, T='00:02:00')
