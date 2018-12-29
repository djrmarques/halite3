class Ship:
    ''' Ship Class '''

    def __init__(self):
        ship.x = x
        ship.y = y
        ship.halite_amount = 0

    def move(self, direction):
        ''' 
        Move into a certain direction 
        direction is a tuple like (0, -1)
        '''
        ship.x += direction[0]
        ship.y += direction[1]

    def collect_halite(self):
        ''' Collects halite from the field '''
        self.halite += 0.25*field.loc[ship.x, ship.y]
        field.loc[ship.x, ship.y] *= 0.75

        if self.halite > 1000:
            self.halite = 1000
