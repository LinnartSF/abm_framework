""""

This module is used to create standardized animations from the database containing ABM simulation results generated with this module.

Wraps matplotlib.pyplot and celluloid

Uses pandas

"""

__author__ = "Linnart Felkl"
__email__ = "LinnartSF@gmail.com"


import matplotlib.pyplot as plt
from celluloid import Camera
import random
import pandas

def warning(msg: str) -> None:
    """ helper function for printing warning """
    print("WARNING: "+msg)

def animate_grid_occupation(df: pandas.DataFrame,
                            population: list = ["all"],
                            color: str = "red",
                            maxtime: int = 0) -> None:
    """ animates grid occulation over simulation time, for the specified population(s), or all populations """
    if maxtime == 0: maxtime = df["simtime"].max()
    
    fig = plt.figure()
    camera = Camera(fig)
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # create scatter plots for the desired population scenario
    if len(population)<1: 
        warning("population list empty or not provided at all for plt_grid_occupation() in stats.py (abm framework)")

    else:
        # add titles
        plt.title(f"grid occupancy for populations: {str(population)}")
        plt.xlabel("columns")
        plt.ylabel("rows")

        if population[0] == "all":
            # use "agents" column data from results database (pandas DataFrame)
            plt.scatter(df[df["agents"]>0]["col"],
                        df[df["agents"]>0]["row"],
                        alpha = df[df["agents"]>0]["agents"]/df["agents"].max(),
                        c = color,
                        label = "all")
        else:
            # add the scatters for each population one by one to the scatter plot, assuming that these populations are also present in the database (pandas DataFrame)
            for pop in population:
                plt.scatter(df[df[pop]>0]["col"],
                            df[df[pop]>0]["row"],
                            alpha = df[df[pop]>0][pop]/df[pop].max(),
                            c = color,
                            label = pop)










# ------------------------------------------------------------------------------------------------------------------------------------------------------------

from matplotlib import pyplot as plt
from celluloid import Camera
import random
import config

# create figure object
fig = plt.figure()

# specify labels
plt.xlabel("coin side")
plt.ylabel("absolute frequency")
plt.title("heads or tail frequency")

# generate animation data
tailheads = [0,0]
xaxpos = [1,2]

camera = Camera(fig)

plt.xticks(xaxpos, labels=["tails","heads"])

for i in range(100):
    
    if random.randint(0,1) > 0:
        tailheads[1] = tailheads[1] + 1
    else:
        tailheads[0] = tailheads[0] + 1

    plt.bar(xaxpos, tailheads, color = ["darkgreen","lightgreen"])
    plt.pause(0.005)
    
    camera.snap()

# build animation from data and save it
animation = camera.animate()
animation.save('animations/coinflipanimation_celluloid.gif', writer='PillowWriter', fps=10)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np

# create figure object
fig = plt.figure()

# set axis limits
plt.xlim(0,10)
plt.ylim(0,1)

# specify labels
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.title("scatter plot animation")

# generate animation data
camera = Camera(fig)
for i in range(10):
    plt.scatter(i, np.random.random())
    plt.pause(0.1)
    camera.snap()

# build animation from data and save it
animation = camera.animate()
animation.save('animations/scatteranimation_celluloid.gif', writer='PillowWriter', fps=2)