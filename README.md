# Disease modelling using a Cellular Automaton model


Dynamic particles          |  Static particles
:-------------------------:|:-------------------------:
<img src="figures\example_simulation_dynamic_small.gif" alt="drawing" width="400"/>  |  <img src="figures\example_simulation_static_small.gif" alt="drawing" width="400"/>
<img src="figures\tp_0.133_match_peak_I.jpg" alt="drawing" width="400" />  |  <img src="figures\tp_0_500_days.jpg" alt="drawing" width="400"/>


## Usage
An example of all of these steps can be found [here](example_notebook.ipynb).
* Install requeriments `pip install -r requeriments.txt`
* Instantiate the `Grid` object:
```py
# Example parameters
g = Grid(nrows, ncols, num_part=10000, init_infected=5, 
            infectious_radius=1, lockdown_at=lock_a, 
            tp_chance=0.3, lockdown_dur=lock_dur)
```

### Rendering simulation
* Initialize the visualization
```py
plt.ion()  
im = isns.imgplot(g.grid, origin="lower", ax=ax, vmin=0, vmax=State.max_value(), 
        cmap="deep", cbar_label="Particle state", despine=True,
        cbar_ticks=range(State.max_value()))
    
def init():
    im.images[0].set_data(np.zeros((nrows, ncols)))
    g.make_simulation(n_frames)

def animate(i):
    im.images[0].set_data(g.history[i])
    im.set(title = f'CA simulation, day {i+1}',)
    return im

anim = animation.FuncAnimation(fig, animate, init_func=init, 
                                frames=tqdm(range(n_frames)), interval=250)
```
* *A)* Visualize on notebook
```py
HTML(anim.to_jshtml())
```
* *B)*  Save to gif
```py
f = r"path/to/file.gif" 
writergif = animation.PillowWriter(fps=10) 
anim.save(f, writer=writergif)
plt.close()
```

### Plotting population graphs (SEIR style)
```py
color_list = ["blue","red","green","purple"]
cmap = colors.LinearSegmentedColormap.from_list("", color_list)
sns.lineplot(data=g.pd_stats,palette=color_list ).set(title = 'CA model', xlabel = 'Days', ylabel = 'Population')
`` 

## Parameters
### Grid
* `nx`: Number of columns (`int`).
* `ny`: Number of rows (`int`).
* `num_part`: Number of particles (`int`).
* `init_infected`: Number of initial infected particles(`int`).
* `latent_tuple`: Duration (days) of exposed period, (mean, std) (`tuple`: `float`, `float`).
* `remove_tuple`: Duration (days) of infectious period, (mean, std) (`tuple`: `float`, `float`).
* `tp_chance`: Chance of particle to teleport to a random position (`float`).
* `infectious_radius`: How far will infectious particle spread to susceptible particles (`int`).
* `lockdown_at`: First day of lockdown (`int`).
* `lockdown_dur`: Duration of lockdown (`int`).
