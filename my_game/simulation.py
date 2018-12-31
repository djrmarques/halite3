import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial.distance import cdist

# Read Map
df = pd.read_csv("seed1.csv", header=None).transpose()

# Starting Position
start_coord = (16, 8)

# Current targets
current_targets = []

# Threshold for a square to be consideres empty
htresh = 50

# Get the distance matrix
d = cdist([a for a in np.ndindex(32, 32)],
          [start_coord],
          metric='cityblock').reshape(32, 32)

df.values[df.values < htresh] = 0

val = np.divide(df.values, np.square(d))

m = plt.matshow(val)
plt.colorbar(m)
plt.show()
