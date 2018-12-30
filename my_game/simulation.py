import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from time import sleep

# Import all the custom entities
from entities import *

# All the custom functions
from aux import *

# Set Turn Limit
n_turns = 20

# Begin Simulation
# Stores Ships
ships = {}
# Create initial ship
ships[1] = Ship(16, 18)

# Shipyard
shipyard = Shipyard(16, 18)

# Read Map
df = pd.read_csv("map.csv", header=None).transpose()

# Remove all halite from the square with the shipyard
df.loc[shipyard.y, shipyard.x] = 0

# Start simulation
for _ in range(n_turns):

    # Call all ships
    for ship in ships.values():
        # Calculates value for all each ship
        cell_values = map_eval(df.values.copy(), ship.position)

        # Select the highest value square
        bx, by = np.where(cell_values == cell_values.max())

fig, ax = plt.subplots(2, 1, tight_layout=True)
mat = ax[0].matshow(cell_values)
mat2 = ax[1].matshow(df)
plt.show()
