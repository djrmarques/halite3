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

# Custom Functions
# These need to be here because it needs to read the game_map object
# Create the val for every cell in the map

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Jules")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # NDarray with the amount of halite in each cell
    map_eval = eval_map(game_map)

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    # Ship Status
    ship_status = {}

    for ship in me.get_ships():
        # Check if ship is full
        logging.info("Ship {} has {}".format(ship.id, ship.halite_amount))

        # Assign new ships to explore
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"

        # Check if return condition is met
        if (drop_condition(ship)):
            ship_status[ship.id] = "returning"
        else:
            # Exploration
            # Assign target to ship
            max_pos = ship_scan(ship.position, map_eval)

            logging.info("Moving ship {} to {}, {}".format(ship.id, max_pos.x, max_pos.y))

            # Check if it is already there
            if max_pos == ship.position:
                command_queue.append(ship.stay_still())
            else:
                command_queue.append(ship.move(game_map.naive_navigate(ship, max_pos)))

        # Return to base
        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:

                # Check if the current spot is rich on halite
                # If so, then collect form it instead of moving away
                if (game_map[ship.position].halit_amount > 200 and
                    game_map[ship.position] != me.shipyard.position
                    ):
                    command_queue.append(ship.stay_still)
                else:
                    move = game_map.naive_navigate(ship, me.shipyard.position)
                    command_queue.append(ship.move(move))

    # Try to control one ship first
    if (me.halite_amount >= constants.SHIP_COST and # If there is enough halite for a new ship
        not game_map[me.shipyard].is_occupied and  # Shipyard not occupied
        len(me.get_ships()) < max_n_ships  # Maximum Number of ships
    ):

        command_queue.append(me.shipyard.spawn())

    logging.info("SHIPS: ", ship_status)
    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
