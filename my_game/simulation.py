import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import dijkstra

# Read Map
df = pd.read_csv("map.csv", header=None).transpose()

d = np.multiply(df.values.copy(), 0.1)
d = d[:5, :5]

def best_route(start, end):
    ''' Determines the best route '''
    spat

start = (4, 4)
end = (0, 0)

dij = dijkstra(d, indices=(start, end))

plt.matshow(d)
plt.show()
