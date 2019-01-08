#!/bin/sh
cd ~/Documents/halite/
rm replays/*
./halite --replay-directory replays/ --turn-limit 324 -s 1 -vvv --width 48 --height 48 "python3 bot1/MyBot.py"  "python3 old-bot/MyBot.py" "python3 old-bot/MyBot.py" "python3 old-bot/MyBot.py"
        
