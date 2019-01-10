# This bot does nothing just for testing

# Import the Halite SDK, which will let you interact with the game.
import hlt

# Import the aux file
from aux import *

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("USELESS BOT")

while True:

    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    game.end_turn([])
