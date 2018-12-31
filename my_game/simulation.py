import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read Map
df = pd.read_csv("seed1.csv", header=None).transpose()

start_coord = (16, 16)

plt.matshow(df)
plt.show()
