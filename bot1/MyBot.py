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

# To calculate the mahatan distance between all the cells in the map
from scipy.spatial.distance import cdist

# Custom Functions
# These need to be here because it needs to read the game_map object
# Create the val for every cell in the map

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Main Bot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # Starts timer
    t = process_time()

    # Next positions
    # This will store the next bot positions and will be used by pathfind 
    # To select the next route and avoid crashes with my own ships
    next_pos = []

    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # NDarray with the amount of halite in each cell
    # All the value bellow the treshold are assigned the halite value of 0 so that
    # that cell value is also 0
    halite_amount = np.array([[c.halite_amount for c in row] for row in game.game_map._cells])
    halite_amount[halite_amount < htresh] = 0

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    # Cycle trhough each ship
    for ship in me.get_ships():

        # If the ship was just created
        if not ship.status:

            # Assign target to ship
            current_targets = next_target(ship, halite_amount, current_targets)

            # Get the direction to the target
            td, next_pos = pathfind(ship.position, ship.target, next_pos)

            # Move in that direction
            command_queue.append(ship.move(td))

            # Change ship status to moving
            ship.status = "moving"

            logging.info("Ship {} assigned to {}.".format(ship.id, (ship.target.x, ship.target.y)))
        
        # If ship is moving
        elif ship.status == "moving":

            # Check if ship is already in target
            if (ship.position == ship.target):
                # Ship on target, start mining

                # Move in that direction
                command_queue.append(ship.stay_still())

                # Change ship status to extracting
                ship.status = "extracting"
                logging.info("Ship {} reached extraction point at {}.".format(ship.id, (ship.target.x, ship.target.y)))

            # If it's not already in the position, go there
            else:
                # Get the direction to the target
                td, next_pos = pathfind(ship.position, ship.target, next_pos)

                # Move in that direction
                command_queue.append(ship.move(td))

        # If ship is extracting at the target
        # The second condition is unnecessary
        elif (ship.status == "extracting" and
              ship.position == ship.target
        ):

            # If the spot halite amount is under the treshold or
            # the ship is not full, find new target
            if (game_map[ship.position].halite_amount < htresh and
                not ship.is_full
            ):
                # Get new target
                # Assign new target to ship
                current_targets = next_target(ship, halite_amount, current_targets)

                # Get the direction to the target
                td, next_post = pathfind(ship.position, ship.target, next_pos)

                # Move in that direction
                command_queue.append(ship.move(td))

                # Change ship status to moving
                ship.status = "moving"

            # If the ship is full, return to base
            elif (ship.is_full):
                # Change ship status to returning
                ship.status = "returning"

                # Change target
                ship.target = me.shipyard.position
                logging.info("Ship {} returning to base.".format(ship.id))

            elif (game_map[ship.position].halite_amount >= htresh):
                # Continue mining
                command_queue.append(ship.stay_still())

            else:
                raise Exception("Unknown condition in with ship {}".format(ship.id))

        # If the ship is returning
        if (ship.status == "returning"):

            # If the ship is not yet in the shipyard
            if ship.position != ship.target:
                # Get the direction to the shipyward
                td, next_pos = pathfind(ship.position, ship.target, next_pos)

                # Move in to shipyard
                command_queue.append(ship.move(td))

            # If ship already in the shipyard
            elif ship.position == ship.target:

                # Assign target to ship
                current_targets = next_target(ship, halite_amount, current_targets)

                # Get the direction to the target
                td, next_pos = pathfind(ship.position, ship.target, next_pos)

                # Move in that direction
                command_queue.append(ship.move(td))

                # Change ship status to moving
                ship.status = "moving"

                logging.info("Ship {} assigned to {}.".format(ship.id, (ship.target.x, ship.target.y)))


    # Conditions for spawning new ships
    if (me.halite_amount >= constants.SHIP_COST and # If there is enough halite for a new ship
        not game_map[me.shipyard].is_occupied and  # Shipyard not occupied
        len(me.get_ships()) < max_n_ships  # Maximum Number of ships
    ):

        command_queue.append(me.shipyard.spawn())

    # Log in elapsed_time
    elapsed_time = process_time() - t
    logging.info("Loop Elapsed Time: {}".format(elapsed_time))

    game.end_turn(command_queue)
