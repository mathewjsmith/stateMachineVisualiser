from statemachine_visualiser.statemachine import StateMachine
from statemachine_visualiser.server import StateMachineServer


def build_statemachine(server: StateMachineServer):
    """
    Build the state-machine hosted on the `server`.

    This is achieved by, for each state encountered, "expanding" the next transition of that state that has not yet been
    expanded. If all three of the current state's transitions have been expanded, a breadth-first search is performed to
    find a path to the nearest known state that is not fully expanded. This is repeated until all states are fully
    expanded.
    """
    sm = StateMachine()
    state = server.get_state()

    while True:
        transition = next_transition(state, sm)
        next_state = server.apply_transition(transition)

        sm.add_transition(state, next_state, transition)

        if next_state == 'Z':
            next_state = server.get_state()

        if fully_expanded(next_state, sm):
            search_result = find_unexpanded(next_state, sm)

            if not search_result:
                break
            else:
                next_state, path = search_result
                move_to_state(path, server)

        state = next_state

    return sm


def next_transition(state, sm):
    """
    Find the next transition of `state` that has not yet been expanded.
    """
    return len(sm.get_transitions(state)) + 1


def fully_expanded(state, sm):
    """
    Determine if the given `state` is fully expanded.
    """
    return len(sm.get_children(state)) == 3 or state == 'Z'


def find_unexpanded(state, sm):
    """
    Perform a breadth-first search from `state` to find the nearest state that is not fully expanded.
    """
    queue = [state]
    parents = {state: None}

    while queue:
        state = queue.pop(0)

        if not fully_expanded(state, sm):
            path = construct_path(state, parents, sm)
            return state, path

        for s in sm.get_children(state):
            if s not in parents:
                parents[s] = state
                queue.append(s)

    return None


def construct_path(state, parents, sm):
    """
    Reconstruct the shortest path to `state` from the given dictionary of `parents`.
    """
    path = []
    parent = parents[state]

    while parent:
        transition = get_transition_no(parent, state, sm)
        path.append(transition)
        state = parent
        parent = parents[state]

    path.reverse()

    return path


def get_transition_no(parent, child, sm):
    """
    Find the number of the transition from `parent` to `child`.

    In the underlying graph structure, edges are stored in the form `(parent, child, t)` where t is the transition
    number.
    """
    transitions = sm.get_transitions(parent)
    transition = next(t for (a, b, t) in transitions if b == child)

    return int(transition)


def move_to_state(path, server):
    """
    Execute the given `path`, which is a sequence of transitions, on the `server` to bring it to the desired state.
    """
    for trans in path:
        server.apply_transition(trans)
