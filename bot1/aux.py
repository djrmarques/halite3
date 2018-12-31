# For general stuff
import numpy as np

# Calculate the cityblock distance
from scipy.spatial.distance import cdist

# Positional Objects
from hlt.positionals import Position, Direction

# Debug info
import logging

''' Custom Variables '''
# Maximum number of ships
max_n_ships = 1

# Threshold for a square to be consideres empty
htresh = 50

# Current Targets
# Stores the current targets of all the ships
# This will avoid colisions (hopefully)
current_targets = []

''' Custom Functions '''
# Navigation functions
def pathfind(start, end):
    ''' 
    Returns a single direction for the ship to move
    to reach a certain target
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


def next_target(ship, hal, current_targets):
    ''' Chooses the next target for the ship. Returns a Position'''

    # Get the cityblock distance matrix
    d = cdist([a for a in np.ndindex(hal.shape)],
              [[ship.position.x, ship.position.y]],
              metric='cityblock').reshape(hal.shape)

    # Value for each cell
    val = np.divide(hal, np.square(d))

    # Assigns the val of the current square as 0
    val[ship.position.x, ship.position.y] = 0

    # Find the maximum value cell
    by, bx = np.where(val == val.max())
    logging.info("\ncoords:{}\nval{}\nhal{}".format((ship.position.x, ship.position.y),
                                                  val[by, bx],
                                                  hal[by, bx]))

    # Set new ship target
    ship.target = Position(bx[0], by[0])

    return  current_targets
