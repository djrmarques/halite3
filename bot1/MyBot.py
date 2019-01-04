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
    unpassable = {}

    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # NDarray with the amount of halite in each cell
    hal = np.array([[c.halite_amount for c in row] for row in game.game_map._cells])

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    # Organize ship is such as the thips that a currenyly extracting are first
    # This will help prevent crashes 
    ships = sorted(me.get_ships(), key= lambda ship: order_ships(ship, game_map))

    # Loggins info ships order
    logging.info("{}".format([(ship.id, ship.status) for ship in ships]))

    # Cycle through each ship
    for ship in ships:

        # Ship is moving for extraction
        if ship.status == "moving":
            # Check if the ship reached the target
            if ship.position == ship.target:
                ship.status="extracting"

            # Move to target
            else: 
                direction, unpassable = pathfind(ship, hal, unpassable)
                command_queue.append(ship.move(direction))

        # Ship is extracting
        if ship.status == "extracting":
            # The ship is full
            if ship.is_full:
                logging.info("Ship {} returning to base".format(ship.id))
                ship.target = me.shipyard.position
                ship.status = "returning"

            # The cell will be bellow the treshold on the next turn
            # and the ship is not full
            elif (0.75 * game_map[ship.position].halite_amount < htresh and 
                  not ship.is_full
            ):
                # Aquire next target
                ship.status = None
                command_queue.append(ship.stay_still())
                unpassable[ship.id] = ship.position

            # Check if the ship will be full on the next turn
            elif (0.25 * game_map[ship.position].halite_amount + ship.halite_amount >= 999
            ):
                # Aquire next target
                logging.info("Ship {} returning to base on the next turn".format(ship.id))
                ship.target = me.shipyard.position
                ship.status = "returning"
                command_queue.append(ship.stay_still())
                unpassable[ship.id] = ship.position

            # Ship will continue extracting
            elif (game_map[ship.position].halite_amount >= htresh and 
                  not ship.is_full
            ):
                command_queue.append(ship.stay_still())
                unpassable[ship.id] = ship.position

        # Ship is returning to base
        if (ship.status == "returning" and
        ship.id not in [int(a.split()[1]) for a in command_queue]):
            # Check if ship is in the shipyard
            if ship.position == me.shipyard.position:
                # Means it will acquire a new objective and move in that direction
                ship.status = None

            # Move to target
            else: 
                direction, unpassable = pathfind(ship, hal.copy(), unpassable)
                command_queue.append(ship.move(direction))

        # Aquire new target and move in that direction
        if not ship.status:
            # Assign target to ship
            current_targets = next_target(ship, hal.copy(), current_targets)

            logging.info("Ship {} assigned to {}.".format(ship.id, (ship.target.x, ship.target.y)))

            # Change ship status to moving
            ship.status = "moving"

            # Check if the ship has nothing to do yet
            if ship.id not in [int(a.split()[1]) for a in command_queue]:

                # Get the direction to the target
                td, unpassable = pathfind(ship, hal.copy(), unpassable)

                # Move in that direction
                command_queue.append(ship.move(td))


    # Conditions for spawning new ships
    if (me.halite_amount >= constants.SHIP_COST and # If there is enough halite for a new ship
        len(me.get_ships()) < max_n_ships and  # Maximum Number of ships
        not game_map[me.shipyard].is_occupied and  # Shipyard not occupied
        me.shipyard.position not in [pos for pos in unpassable.values()]  # Shipyard not occupied
    ):

        command_queue.append(me.shipyard.spawn())

    # Log Ship Targets
    logging.info("Ship Targets:\n{}".format(
        ["{}:{}".format(ship.id, ship.target) for ship in me.get_ships()]))

    # Log Ship Positions at the end of the turn
    logging.info("Positions ocupied in the next turn:\n{}".format(
        ["{}:{}".format(id, pos) for id, pos in unpassable.items()]))

    # Log command queue
    logging.info("Command Queue:\n{}".format(command_queue))

    # Log in elapsed_time
    elapsed_time = process_time() - t
    # logging.info("Loop Elapsed Time: {}".format(elapsed_time))

    game.end_turn(command_queue)
