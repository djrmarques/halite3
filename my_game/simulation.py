import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Halite
df = pd.read_csv("map_eval,csv", header=None).transpose()

ships()

def value_each_cell():
    ''' Simulates the value for each cell '''
    pass

plt.matshow(df.values)
plt.show()

