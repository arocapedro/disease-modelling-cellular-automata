from enum import IntEnum

class State(IntEnum):
    SUSCEPTIBLE = 1
    EXPOSED = 2
    INFECTIOUS = 3
    REMOVED = 4

    def get_values():
        return list(map(int, State))
    
    def max_value():
        return State.get_values()[-1]
