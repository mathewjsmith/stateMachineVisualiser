from statemachine_visualiser.server import StateMachineServer
from statemachine_visualiser.builder import build_statemachine
import constants


if __name__ == '__main__':
    with StateMachineServer(constants.HOST, constants.PORT) as server:
        sm = None

        try:
            print("Building the state-machine...")
            sm = build_statemachine(server)
        except Exception as e:
            raise e
        finally:
            sm.draw()
