#!/bin/bash

gnome-terminal --tab --title="Actuator_1" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_1; $SHELL'
gnome-terminal --tab --title="Actuator_2" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_2; $SHELL'
gnome-terminal --tab --title="Sensor_1" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_1; $SHELL'
gnome-terminal --tab --title="Sensor_2" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_2; $SHELL'
gnome-terminal --tab --title="Master" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py master; $SHELL'