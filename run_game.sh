#!/bin/sh
cd ~/Documents/halite/
rm replays/*
./halite --replay-directory replays/ --turn-limit 50  -s 1 -vvv --width 32 --height 32 "python3 MyBot.py" "python3 MyBot.py"
