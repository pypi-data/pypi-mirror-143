"""
Code to draw plot for the documentation.

This plots an example of an evolutionary stable strategy.

The code should match the reference code in the documentation.
"""
import matplotlib.pyplot as plt
import numpy as np

import nashpy as nash

A = np.array([[4, 3], [2, 3]])
game = nash.Game(A)
epsilon = 1 / 10
y0 = np.array([1 - epsilon, 0 + epsilon])
timepoints = np.linspace(0, 10, 1000)

plt.plot(game.replicator_dynamics(y0=y0, timepoints=timepoints))
plt.xlabel("Timepoints")
plt.ylabel("Probability")
plt.title("Probability distribution of strategies over time")
plt.legend([f"$s_{0}$", f"$s_{1}$"])

plt.savefig("main.svg", transparent=True)
