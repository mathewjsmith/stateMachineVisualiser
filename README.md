# State Machine Visualiser

The state-machine is built by, for each state encountered, "expanding" the next transition from the state that has not yet been expanded. If all three of the current state's transitions have already been expanded, a breadth-first search is performed to find a path to the nearest known state that is not yet fully expanded. This is repeated until all states are fully expanded.

The diagram of the most recently generated state-machine can be found [here](diagrams/statemachine.pdf).

Server details should be specified as `HOST` (string) and `PORT` (int) variables in a `constants.py` file in the root directory of the project.
