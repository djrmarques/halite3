#!/bin/sh
cd ~/Documents/halite/
rm replays/*
./halite --replay-directory replays/ --turn-limit 100  -s 1 -vvv --width 32 --height 32 "python3 bot1/MyBot.py" "python3 bot2/MyBot.py"
