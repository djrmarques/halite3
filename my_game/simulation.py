import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read Map
df = pd.read_csv("seed1.csv", header=None).transpose()

# Starting Position
start_coord = (16, 16)

# Current targets
current_targets = []

# Threshold for a square to be consideres empty
htresh = 50

def find_1000(halite_amount, ship_position, current_targets):
    ''' 
    Returns a list of the nearest positions where the ship can get 
    1000 halite, disregarding cells already assigned to other ships
    '''
    x, y = ship_position
    # Change in the real routine
    # x, y = ship_position.x, ship_position.y

    # Stores positions to return
    pos_list = []

    # Divide the array in equal parts the all sum to 1000

    return pos_list, current_targets + pos_list

def nearest_cell(halite_amount, start, pos_list, current_targets, hal=0):
    ''' Recursive function that seeks the next nearest_cell cell for mining until 1000 is reached '''
    
                 

# Subtract the treshold in every cell
pos_list = find_1000(df.values.copy()-htresh, start_coord, [])

plt.matshow(df)
plt.show()
