# For general stuff
import numpy as np

# Calculate the cityblock distance
from scipy.spatial.distance import cdist

# Positional Objects
from hlt.positionals import Position, Direction

# Debug info
import logging


''' custom variables '''
# Maximum number of ships
max_n_ships = 2

# Threshold for a square to be consideres empty
htresh = 40

# Current Targets
# Stores the current targets of all the ships
# This will avoid colisions (hopefully)
current_targets = []

''' custom functions '''
# Navigation functions
def pathfind(start, end, next_pos):
    ''' 
    Returns a single direction for the ship to move
    to reach a certain target.
    Next pos stores locations of other ships
    '''

    # Stores the possible directions
    possible_directions = []

    # Calculate difference in coordinates
    dy = end.y - start.y
    dx = end.x - start.x

    # Determine the possible positions
    if dx < 0:
        possible_directions.append(Direction.West)
    if dx > 0:
        possible_directions.append(Direction.East)
    if dy > 0:
        possible_directions.append(Direction.South)
    if dy < 0:
        possible_directions.append(Direction.North)

    # position.directional_offset(direction)
    # Checks if the possible directions are already taken by anothers ships
    for d in possible_directions:
        if (start.directional_offset(d) not in next_pos):
            next_pos.append(start.directional_offset(d))
            return d, next_pos

    # If no directoin available, stay still
    next_pos.append(start)
    return 'o', next_pos

    # Needs to return also the next pos

def next_target(ship, hal, current_targets):
    ''' Chooses the next target for the ship. Returns a Position'''

    # Get the cityblock distance matrix
    d = cdist([a for a in np.ndindex(hal.shape)],
              [[ship.position.y, ship.position.x]],
              metric='cityblock').reshape(hal.shape)

    # Value for each cell
    val = np.divide(hal, np.square(d))

    # Target positions. the current targets contains Position objects
    # If the list is not empty
    if current_targets:
        for pos in current_targets:
            val[pos.y, pos.x] = 0

    # Assigns the val of the current square as 0
    val[ship.position.y, ship.position.x] = 0

    # Find the maximum value cell
    by, bx = np.where(val == val.max())

    # Set new ship target
    ship.target = Position(bx[0], by[0])

    # Apend to current targets
    current_targets.append(Position(bx[0], by[0]))

    return  current_targets
