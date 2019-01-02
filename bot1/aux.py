# For general stuff
import numpy as np

# Calculate the cityblock distance
from scipy.spatial.distance import cdist

# Positional Objects
from hlt.positionals import Position, Direction

# Debug info
import logging

# For the heuristic
from math import sqrt


''' Custom Variables '''
# Maximum number of ships
max_n_ships = 3

# Threshold for a square to be consideres empty
htresh = 40

# Stores the selected targets
current_targets = []

''' Custom Functions '''
# Lambda functions for value
# Heuristc
h = lambda end, start: 500*sqrt(abs(start[0] - end[0])**2 + abs(start[1] - end[1])**2)
# val = lambda start, target, m: m[start] + h(target, start)

def val(start, target, m):
    # logging.info("s: {} with {} + {} = {}".format(start, m[start], h(target, start), m[start] + h(target, start)))
    return m[start] + h(target, start)

def pathfind(ship, target: Position, m, unpassable: list):
    ''' 
    Determines the best route to target using astar.
    Start and target are Position objects
    '''


    # Get the ship object
    start = ship.position

    # Start position coord tupple
    sx, sy = start.x, start.y

    # Target position coord tupple
    tx, ty = target.x, target.y

    logging.info("Moving Ship {} at {} to target {}".format(ship.id, (sx, sy), (tx, ty)))
    logging.info("  Unpasable: {}".format(unpassable))

    # Get adjacent squares (list with Position objects)
    adj = start.get_surrounding_cardinals()
    
    # Remove adjacent squares that are impassable
    adj = [a for a in adj if a not in unpassable]

    # See if ship can get out of the square
    # If not, return the same position
    # If no squares are available, stay still
    # And add current position to the unpassable list
    if (ship.halite_amount < 0.1 * m[sy, sx] or
        not adj

    ):
        unpassable.append(start)
        return 'o', unpassable

    # Sort Positions by value
    # Get position as tupple
    adj = [(pos.y, pos.x) for pos in adj]

    # DEBUG DELETE THIS
    adj = sorted(adj, key=lambda c: val(c, (ty, tx), m))[0]
    # Get the best direction
    d_tuple = (adj[1]-sx, adj[0]-sy)
    # logging.info("{}".format(d_tuple))

    # need to normalize the tuple in case of something line (0, -31)
    # Probably not the most efficient way of doing this
    if max([abs(a) for a in d_tuple]) == 31:
        d_tuple = tuple([int(a/31) for a in d_tuple])

    direction = Direction.convert(d_tuple)

    # Append new position to unpassable
    unpassable.append(start.directional_offset(d_tuple))

    return direction, unpassable

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
