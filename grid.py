from particle import Particle
from state import State

import random
import numpy as np
from tqdm import tqdm

import pandas as pd

class Grid:
    def __init__(self, nx, ny, num_part, init_infected=1, 
                latent_tuple=(5.2, 3.7), remove_tuple=(2.9, 2.1), tp_chance=0, 
                infectious_radius=2, lockdown_at=0, lockdown_dur=0):

        self.x_size = nx
        self.y_size = ny
        self.clear_grid()
        self.particles = np.zeros(dtype=Particle, shape=(self.grid.shape))
        self.rad = infectious_radius
        self.tp_chance = tp_chance
        self.lock_a = lockdown_at
        self.lock_b = lockdown_at+lockdown_dur
        self.particle_count = num_part
        self.history = []
        print("Grid shape",self.grid.shape)

        population = 0
        for i in tqdm(range(num_part)):
            tries = 0
            x = random.randint(0, nx-1)
            y = random.randint(0, ny-1)
            while (tries != num_part*2 and self.grid[x][y] != 0):
                x = random.randint(0, nx-1)
                y = random.randint(0, ny-1)
                tries += 1
            
            assert tries < 300, "Grid full!"

            part = Particle(x, y, remove_tuple=remove_tuple, latent_tuple=latent_tuple)
            
            self.grid[x, y] = part.state
            self.particles[x, y] = part
            population += 1
        infected = 0
        for i in range(init_infected):
            p = int(0)
            while p == 0: 
                x = random.choice(list(range(0, self.x_size)))
                y = random.choice(list(range(0, self.y_size)))
                p = self.particles[x, y]
            p.change_state(State.INFECTIOUS)
            infected += 1

        print(f"Created {population} particles, {infected} infected")

    def clear_grid(self):
        self.grid = np.array(
                        np.zeros(self.x_size*self.y_size).
                            reshape((self.x_size, self.y_size))
                    )

    def make_simulation(self, days):
        print(f"Simulating for {days} days...")
        self.history = []
        for i in tqdm(range(days)):
            self.update_infection(i)
            self.history.append(self.grid)
        print(f"Generating sim. stats...")
        self.generate_pop_stats()

    def generate_pop_stats(self):
        sus_count=[]; exposed_count=[]; infectious_count=[]; recovered_count=[]; dead_count=[]
        for snapshot in self.history:
            sus_count.append( snapshot[snapshot==State.SUSCEPTIBLE].size )
            exposed_count.append(  snapshot[snapshot==State.EXPOSED].size )
            infectious_count.append(  snapshot[snapshot==State.INFECTIOUS].size )
            recovered_count.append(  snapshot[snapshot==State.REMOVED].size )
        simulation = pd.DataFrame({"susceptible":sus_count, "exposed":exposed_count, 
                "infectious":infectious_count, "removed":recovered_count})
        self.pd_stats = simulation
    
    def update_infection(self, i):
        self.clear_grid()

        #travel sim
        lockdown_reducer = 1
        if self.lock_a <= i <= self.lock_b:
            lockdown_reducer = 0.05
        for i in range(int(self.tp_chance*self.particle_count*lockdown_reducer)):
            p = int(0)
            while p == 0 or p == self: 
                x = random.choice(list(range(0, self.x_size)))
                y = random.choice(list(range(0, self.y_size)))
                p = self.particles[x, y]
            new_x = p.x
            new_y = p.y
            old_x = p.x
            old_y = p.y
            while self.particles[new_x, new_y] != 0:
                new_x = random.randint(0, self.x_size-1)
                new_y = random.randint(0, self.y_size-1)
            p.x = new_x
            p.y = new_y
            self.particles[old_x, old_y] = 0
            self.particles[new_x, new_y] = p
                        
        current_part = self.particles[np.where(self.particles != 0)]
        for p in current_part:
            p.step += 1
            match p.state:
                case State.INFECTIOUS:
                    # spread the disease to others
                    for xi in range(p.x-self.rad, p.x+self.rad+1):
                        for yi in range(p.y-self.rad, p.y+self.rad+1):
                            if not (xi == p.x and yi == p.y) and \
                                    xi < self.x_size and yi < self.y_size:
                                    
                                # if the new particle is susceptible, infect with prob i_c
                                if self.particles[xi, yi] != 0 and \
                                    self.particles[xi, yi].state == State.SUSCEPTIBLE:
                                        
                                    self.grid[xi,yi] = State.EXPOSED
                                    self.particles[xi, yi].change_state(State.EXPOSED)

                    # recover or die D:
                    if p.step * p.remove_rate >= 1: # fully recovered
                        p.change_state(State.REMOVED)
                    else:
                        # still recovering
                        pass
                
                case State.EXPOSED:
                    # advance disease
                    if p.step * p.latent_rate >= 1:
                        p.change_state(State.INFECTIOUS)
                    else:
                        # disease still latent
                        pass
            
            self.grid[p.x,p.y] = p.state
