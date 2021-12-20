#!/bin/bash

gnome-terminal --tab --title="Actuator_1" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_1; $SHELL'
gnome-terminal --tab --title="Actuator_2" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_2; $SHELL'
gnome-terminal --tab --title="Actuator_3" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_3; $SHELL'
gnome-terminal --tab --title="Actuator_4" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_4; $SHELL'
gnome-terminal --tab --title="Actuator_5" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py actuator_5; $SHELL'
gnome-terminal --tab --title="Sensor_1" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_1; $SHELL'
gnome-terminal --tab --title="Sensor_2" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_2; $SHELL'
gnome-terminal --tab --title="Sensor_3" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_3; $SHELL'
gnome-terminal --tab --title="Sensor_4" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_4; $SHELL'
gnome-terminal --tab --title="Sensor_5" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py sensor_5; $SHELL'
gnome-terminal --tab --title="Master" -- bash -c 'cd ../../src; /home/limnglng/anaconda3/bin/python start.py master; $SHELL'