# 538-Distributed-Systems-Project-2021W1-Haptic-Creature-Architecture
Course Project for CPSC 538 2021W1

## Prereq Packages

## Host virtual serial port
Use the following command to create virtual serial port in terminal
`socat -d -d pty,raw,echo=0 pty,raw,echo=0`
Adjust the config for serial connections using the results of above command

## Start a node
To start any node, `cd` to `src` directory and run the following command:
`python start.py <name_of_node>`
where `<name_of_node>` is the same as the name of configuration file under `config/`

For example, to run the master node:
`python start.py master`

Or to run actuator 1:
`python start.py actuator_1`
