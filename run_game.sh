#!/bin/sh
cd ~/Documents/halite/
rm replays/*
./halite --replay-directory replays/ --turn-limit 70 -s 1546633773 -vvv --width 32 --height 32 "python3 bot1/MyBot.py" "python3 old-bot/MyBot.py"
        
