# For calculations
import numpy as np

# Search Radious
sr = 1

# Maximum number of ships
max_n_ships = 1

from hlt.positionals import Position


# Custom Functions
# Scan around the ship for the best spot
def ship_scan(ship_position, eval_map):
    ''' Determines the best spot to get halite '''

    # Create the position objects for the search radious
    for index, x in np.ndenumerate(eval_map):
        eval_map[index] = cell_value(x, index, ship_position)


    bx, by = np.where(eval_map == eval_map.max())

    return Position(bx, by)

def cell_value(hal, pos, ship):
    ''' Evaluates the value a cell considering the distance and halite amount'''
    posx, posy = pos
    return hal / (abs(posx-ship.x) + abs(posy-ship.y))

def drop_condition(ship):
    ''' Boolean for if the ship should return or not '''
    return ship.is_full

# Navigation functions
def caclulate_cost(start, end):
    ''' Calculates the cost of navigating from one spot to the other '''
    pass

def best_route(start, end):
    ''' 
    Returns the best route by considering the halite cost 
    '''
    pass

# Map Info
def eval_map(game_map):
    ''' Returns a ndarray with all the halite on each spot '''

    # Create ndarray
    map_eval = np.zeros([game_map.height, game_map.width])

    for index, x in np.ndenumerate(map_eval):
        map_eval[index] = game_map[Position(*index)].halite_amount

    return map_eval
