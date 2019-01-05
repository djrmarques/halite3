# Script that plays the new vs old bot in a variaety of diferent maps 
# And check if who wins

import subprocess
import re
from numpy.random import randint
import pandas as pd
from itertools import product

# Delete everything from the replay folder
subprocess.run(["rm replays/*"], shell=True)

# Several Parameters to test
size = [32, 48, 56]
n_players = [2, 3, 4]
seeds = randint(1, 50000, 5).tolist()

# Create all the combinations
# Pandas that stores the end results
res = pd.DataFrame(columns=["seed", "n_players", "size", "winner"])

n = len(list(product(seeds, size, n_players)))
counter = 1

# Number of tests entries
for seed, size, n_players in product(seeds, size, n_players):
    # Prints info
    print("Trial {}/{}".format(counter, n))
    print("Seed: {}\nSize: {}\nNPlayers: {}\n".format(seed, size, n_players))
    counter += 1

    players = {1: "'python3 bot1/MyBot.py' 'python3 old-bot/MyBot.py'",
               2: "'python3 bot1/MyBot.py' 'python3 old-bot/MyBot.py'",
               3: "'python3 bot1/MyBot.py' 'python3 old-bot/MyBot.py' 'python3 old-bot/MyBot.py'",
               4: "'python3 bot1/MyBot.py' 'python3 old-bot/MyBot.py' 'python3 old-bot/MyBot.py' 'python3 old-bot/MyBot.py'"}

    # The result is in the stderr
    process = "./halite --replay-directory replays/ -s {} --width {} --height {} {}".format(seed, size, size, players[n_players])

    # ./halite --replay-directory replays/ -s 1546633773 --width 48 --height 48 "python3 bot1/MyBot.py" "python3 old-bot/MyBot.py"

    log = subprocess.run(process,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       shell=True)

    # Decode bytes
    out =  log.stderr.decode("utf-8")

    for p in re.findall(r".*rank 1.*", out):
        # Get the name of the player
        winner = p.split(',')[1].strip()[1:-1]

        # Next index 
        n_index = res.shape[0]+1
        res.loc[n_index, :]=[seed, n_players, size, winner]

        # Only get the first 
        # This is not necessary but wtv
        break

print(res["winner"].value_counts())
