import numpy as np
from state import State

class Particle():
    def __init__(self, x, y, remove_tuple, latent_tuple):
        self.x = x
        self.y = y
        self.step = 0
        self.state = State.SUSCEPTIBLE

        self.remove_rate = 1/(np.random.uniform(remove_tuple[0], remove_tuple[1]))
        self.latent_rate = 1/(np.random.uniform(latent_tuple[0], latent_tuple[1]))
    
    def change_state(self, new_state):
        self.step = 0
        assert new_state in State.get_values(), f"Value {new_state} not found!"
        
        self.state = new_state
        