import numpy as np
from scipy.spatial.distance import cdist

# Custom Functions
#  Evaluate the value for each cell for a given ship
def map_eval(field, ship):
    ''' Returns the value for each cell for a ships location '''
    d = cdist([a for a in np.ndindex(field.shape)],
                  [ship],
                  metric="cityblock").reshape(field.shape)

    d = np.divide(field, np.sqrt(d))
    d[d == np.inf] = 0
    return d

