class Ship:
    ''' Ship Class '''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.halite_amount = 0
        self.position = (self.x, self.y)

    def move(self, direction):
        ''' 
        Move into a certain direction 
        direction is a tuple like (0, -1)
        '''
        self.x += direction[0]
        self.y += direction[1]

    def collect_halite(self, field):
        ''' Collects halite from the field '''
        self.halite += 0.25*field.loc[self.x, self.y]
        field.loc[self.x, self.y] *= 0.75

        if self.halite > 1000:
           self.halite = 1000

        return field

class Shipyard:
    ''' Shipyard class '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
