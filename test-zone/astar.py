import numpy as np
import matplotlib.pyplot as plt
from time import process_time
from scipy.spatial.distance import cdist
from random import choice

class Ant:
    ''' Used by the ant colony class '''
    def __init__(self, pos):
        self.hal = 0
        self.pos = pos

    def get_adj(self):
        x, y = self.pos
        return [((x+dx)%ms, (y+dy)%ms)
                for dx, dy in
                [[0, 1], [0, -1], [1, 0], [-1, 0]]]

class AntCol:
    ''' Solves ant colony '''

    def __init__(self, hal, d, start):
        self.d = d
        self.h = hal
        self.n_ants = 30
        self.start = start
        self.ants = [Ant(start) for _ in range(self.n_ants)]
        self.ph = np.zeros(hal.shape)

    def next_pos(self, adj):
        ''' Determines the next position for an ant '''
        p = np.array(adj)
        return choice(adj, p)


    def solve(self):
        ''' Returns a path '''

        # Cycle trough every ant
        for ant in self.ants:
            pass
            

            



# Get the map
# THe array is switched to get the same coordinates as the game
m = np.load("hal.npy").T
ms = m.shape[1]

# Get the distance matrix
center = [int(ms/2), int(ms/2)]
d = cdist([center],
          [a for a in np.ndindex(m.shape)],
          metric="cityblock").reshape(m.shape).T

pos = (8, 16)
shift = [pos[0]-center[0], pos[1]-center[1]]
d = np.roll(d, shift, axis=[1, 0])

# Returns the best route
route = ant_colony(m.copy(), d.copy(), pos)

# mat = plt.matshow(d)
# plt.colorbar(mat)
# plt.show()

