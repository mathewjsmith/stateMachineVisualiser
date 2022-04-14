from socket import socket, AF_INET, SOCK_STREAM
from abc import ABC


class Server(ABC):
    def get_state(self):
        pass

    def apply_transition(self, transition):
        pass


class StateMachineServer(Server):
    def __init__(self, host, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port

    def get_state(self):
        state = self.sock.recv(1024).strip(b'\n').decode()

        if len(state) > 1:
            state = state[0]

        return state

    def apply_transition(self, transition):
        self.sock.send(f'{transition}\n'.encode())
        return self.get_state()

    def __enter__(self):
        self.sock.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


class TestInstance(Server):
    def __init__(self):
        self.graph = {
            'A': ['B', 'C', 'Z'],
            'B': ['C', 'A', 'Z'],
            'C': ['Z', 'B', 'A'],
            'Z': ['A']
        }
        self.state = 'A'

    def get_state(self):
        if self.state == 'Z':
            self.state = 'A'

        return self.state

    def apply_transition(self, transition):
        self.state = self.graph[self.state][transition - 1]
        return self.state

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
