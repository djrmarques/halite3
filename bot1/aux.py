# For general stuff
import numpy as np

# Calculate the cityblock distance
from scipy.spatial.distance import cdist

# Positional Objects
from hlt.positionals import Position, Direction

# Debug info
import logging

# For the heuristic
from math import sqrt, trunc

''' Custom Variables '''
# Threshold for a square to be consideres empty
htresh = 40

# Stores the selected targets
current_targets = []

# Increment this variable every turn 
# There is a way of getting this from the game but wtv
turn = 1

''' Custom Functions '''
# NAVIGATION
# Lambda functions for value
# Heuristc

def h(end, start, size):
    ''' Calculates the toroidal distance between coordinates '''

    dx = abs(end[0] - start[0])
    dy = abs(end[1] - start[1])

    if (dx > 0.5*size):
        dx = size-dx
    if (dy > 0.5*size):
        dy = size-dy

    return 3000*(dx**2 + dy**2)

# val = lambda start, target, m: m[start] + h(target, start, m.shape[0])

def val(start, target, m):
    # logging.info("Direction {}, map size {},  has a value of {} + {} = {}".format(start, m.shape, m[start], h(target, start, m.shape[0]),  m[start] + h(target, start, m.shape[0]))) 

    return m[start] + h(target, start, m.shape[0])

def pathfind(ship, m, unpassable: list):
    ''' 
    Determines the best route to target using astar.
    Start and target are Position objects
    '''

    size = m.shape[0]

    # Get the ship position
    start = ship.position

    # Get the target
    target = ship.target

    # Start position coord tupple
    sx, sy = start.x, start.y

    # Target position coord tupple
    tx, ty = target.x, target.y

    # Get adjacent squares (list with Position objects)
    adj = start.get_surrounding_cardinals()
    
    # Remove adjacent squares that are unpassable (occupied)
    # logging.info("Ship {}: Unpassable {}".format(ship.id, unpassable))
    adj = [a for a in adj if a not in unpassable.values()]

    # See if ship can get out of the square
    # If not, return the same position
    # If no squares are available, stay still
    # And add current position to the unpassable list
    if (ship.halite_amount < round(0.1*m[sy, sx]) or
        not adj
    ):
        logging.info("Ship {} on square {} with hal: {} needs {} to move and has {}".format(ship.id, (sx, sy), m[sy, sx], 0.1*m[sy, sx], ship.halite_amount))
        unpassable[ship.id]=start
        return 'o', unpassable

    # All the tiles with hal < htresh have value 0
    m[m < htresh] = 0

    # Sort Positions by value
    # Get position as tupple
    adj = [(pos.y, pos.x) for pos in adj]

    # Sort the positions based on val
    adj = sorted(adj, key=lambda c: val(c, (ty, tx), m))[0]

    # Replace with the navigate function
    # Get the best direction
    d_tuple = (adj[1]-sx, adj[0]-sy)
    # logging.info("{}".format(d_tuple))

    # need to normalize the tuple in case of something like (0, -31)
    # Probably not the most efficient way of doing this
    if max([abs(a) for a in d_tuple]) == size-1:
        d_tuple = tuple([int(a/-(size-1)) for a in d_tuple])

    direction = Direction.convert(d_tuple)

    # Append new position to unpassable
    unpassable[ship.id] = (start.directional_offset(d_tuple))

    return direction, unpassable

def next_target(ship, hal, current_targets, game_map):
    ''' Chooses the next target for the ship. Returns a Position'''


    # All the tiles with hal < htresh have value 0
    hal[hal < htresh] = 0

    # Get the cityblock distance matrix
    d = np.zeros(hal.shape)

    # But need to consider the toroidal
    for index in np.ndindex(hal.shape):
        d[index] = game_map.calculate_distance(ship.position, Position(index[1], index[0]))

    # Remove the error
    d[d==0] = 1000
    # value for each cell
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


# MOVE ORDER OF SHIPS IN A TURN 
# Returns the mathantan distance of two positions
d = lambda posx, posy: abs(posx.x - posy.x) + abs(posx.y - posy.y)
def order_ships(ship, game_map):
    if ship.status == "extracting":
        # Order ships by halite in cargo
        # The ones with more cargo move latter 
        # This will help avoiding crashes
        return (game_map[ship.position].halite_amount)
    elif not ship.status:
        return 1001
    elif ship.status == "returning" :
        return 2000 + (1000 - ship.halite_amount)
    elif (ship.status == "moving") :
        # Organize by distance to target
        # This will ensure that ships will not ocupy the targets of other ships as they move there

        # First, the ships that cannot move
        if ship.halite_amount < round(0.1 * game_map[ship.position].halite_amount):
            return 1002
        else:
            return 1003 + game_map.calculate_distance(ship.position, ship.target)

def get_number_ships(hal, htresh, n_players):
    ''' Determines the maximum number of ships '''

    # All the tiles with hal < htresh have value 0
    hal[hal < htresh] = 0

    max_hal_map = hal.sum()
    n_ships = int(max_hal_map/(1000*n_players))
    logging.info("max_hal: {} max_ships: {}".format(max_hal_map, n_ships))

    return n_ships


# INSPIRATON
def is_inspired(ship, enemies_list):
    ''' Determined if a ship is inspired in the current position. Return Bool'''

    # Get all the positions within a radious of 4 from all the ships
    radious = 4

    ships_in_radious = 0

    for dx in np.arange(-radious, radious+1):
        for dy in np.arange(-radious, radious+1):
            nx = ship.position.x+dx
            ny = ship.position.y+dy

            if (nx, ny) in enemies_list:
                ships_in_radious += 1

            if ships_in_radious > 2:
                ship.is_inspired = True
                return 0

    ship.is_inspired = False
