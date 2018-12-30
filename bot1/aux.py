# For calculations
import numpy as np
from scipy.spatial.distance import cdist

# Maximum number of ships
max_n_ships = 1

from hlt.positionals import Position, Direction

# Custom Functions
# Scan around the ship for the best spot

# Navigation functions
def caclulate_cost(start, end):
    ''' Calculates the cost of navigating from one spot to the other '''
    pass

def pathfind(start, end):
    ''' 
    Returns a single direction for the ship to move
    '''
    dy = end.y - start.y
    dx = end.x - start.x

    if dx < 0:
        return Direction.West
    elif dx > 0:
        return Direction.East
    elif dy > 0:
        return Direction.South
    elif dy < 0:
        return Direction.North

# Map Info
def eval_map(halite_amount, ship_position):
    ''' Return Position for the best spot '''

    # Calculate distance from ship position
    d = cdist([a for a in np.ndindex(halite_amount.shape)],
              [(ship_position.x, ship_position.y)],
              metric="cityblock").reshape(halite_amount.shape)

    # Calculate the value
    val_matrix = np.divide(halite_amount, np.sqrt(d, order=4))
    val_matrix[val_matrix == np.inf] = halite_amount[val_matrix == np.inf]

    # Get the best squares
    by, bx = np.where(val_matrix == val_matrix.max())

    return Position(bx[0], by[0])
