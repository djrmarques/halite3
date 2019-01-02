import numpy as np
import matplotlib.pyplot as plt

# Get the map
m = np.load("hal.npy")

# Heuristc value
h = lambda end, start: 100*(abs(start[0] - end[0]) + abs(start[1] - end[1]))
val = lambda start: m[start] + h(target, start)

def get_adjacent_positions(pos):
    ''' Returns a list with adjacent positions '''
    adj = []

    for dis in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        adj.append((pos[0] + dis[0], pos[1] + dis[1]))

    return adj

get_adjacent_positions([0, 0])

def astar(ship_pos, target, m, unavailable_squares):
    ''' Determines the best route to target using astar '''

    # store path coordinates
    path = []

    # Path
    while(ship_pos != target):

        # Append position to list 
        path.append(ship_pos)

        # Current position
        current = ship_pos[0], ship_pos[1] 

        # Get the list ordered by cost
        adj = sorted(get_adjacent_positions(ship_pos), key=val)

        # Remove adjacent squares that are impassable
        adj = [a for a in adj if a not in unavailable_squares]

        # Sets new ship position
        ship_pos = adj[0]

    
    return path


target = [27, 28]
path= astar((16, 8), (27, 28), m, [(16, 9), (16, 10), (17, 9)])

plt.matshow(m)
x = [x[0] for x in path]
y = [x[1] for x in path]
plt.scatter(x, y, c='r')
plt.scatter(*target)
plt.show()
