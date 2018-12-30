#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction, Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

# Import the aux file
from aux import *

# Import time
from time import process_time

# Variables that saves the ship status
ship_status = {}

# Custom Functions
# These need to be here because it needs to read the game_map object
# Create the val for every cell in the map

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Cancer")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # Starts timer
    t = process_time()

    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # NDarray with the amount of halite in each cell
    halite_amount = np.array([[c.halite_amount for c in row] for row in game.game_map._cells])

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []


    for ship in me.get_ships():

        # Assign new ships to explore
        if ship.id not in ship_status.keys():
            ship_status[ship.id] = "returning"
            logging.info("New Ship Created")

        # Check if return condition is met
        if (ship.halite_amount > 500):
            ship_status[ship.id] = "returning"
            logging.info("Ship {} return to base with {}".format(ship.id, ship.halite_amount))
            
        elif (ship_status[ship.id] == "exploring" and
              ship.halite_amount <= 500
        ):
            # Explore
            # Check if it is already there
            if ship.target == ship.position:
                logging.info("Ship: {}, harvesting halite at target".format(ship.id))
                command_queue.append(ship.stay_still())
            else:
                logging.info("Ship: {}, going to target".format(ship.id))
                direction = pathfind(ship.position, ship.target)
                command_queue.append(ship.move(direction))

        # Return to base
        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:

                # Change ship status
                ship_status[ship.id] = "exploring"

                # Assign target to ship
                best_pos = eval_map(halite_amount, ship.position)
                ship.target = best_pos
                direction = pathfind(ship.position, ship.target)
                command_queue.append(ship.move(direction))

                # Print the new ship target
                logging.info("Ship {} targeted at {}, {}".format(ship.id, best_pos.x, best_pos.y))

            else:
                move = pathfind(ship.position, me.shipyard.position)
                command_queue.append(ship.move(move))
                # Print the new ship target
                logging.info("Ship {} returning to shipyard".format(ship.id))

    # Try to control one ship first
    if (me.halite_amount >= constants.SHIP_COST and # If there is enough halite for a new ship
        not game_map[me.shipyard].is_occupied and  # Shipyard not occupied
        len(me.get_ships()) < max_n_ships  # Maximum Number of ships
    ):

        command_queue.append(me.shipyard.spawn())

    # Log in elapsed_time
    elapsed_time = process_time() - t
    logging.info("Loop Elapsed Time: {}".format(elapsed_time))

    game.end_turn(command_queue)
