#!/bin/bash
gnome-terminal --tab --title="Clear_Logs" -- bash -c 'cd ../../logs/; rm -rf *; $SHELL'