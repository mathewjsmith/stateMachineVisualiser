from pygraphviz import AGraph


class StateMachine:
    def __init__(self):
        self.graph = AGraph(directed=True, strict=False)
        self.graph.add_edge('Z', 'A', key=1)

    def add_state(self, state):
        self.graph.add_node(state)

    def add_transition(self, src, dst, transition):
        self.graph.add_edge(src, dst, key=str(transition), label=str(transition))

    def get_transitions(self, state):
        return self.graph.out_edges(state, keys=True)

    def get_children(self, state):
        return self.graph.out_neighbors(state)

    def draw(self, filename='diagrams/statemachine.pdf'):
        self.graph.layout(prog="dot")
        self.graph.draw(filename)
        print(f'The state-machine diagram has been written to {filename}.')
