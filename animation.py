"""

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
import config

def warning(msg: str) -> None:
    """ helper function for printing warning """
    print("WARNING: "+msg)

def animate_grid_occupation(df: pandas.DataFrame,
                            filename: str,
                            population: list = ["all"],
                            color: str = "red",
                            tpf: float = 0.01, # time per frame
                            mintime: int = 0,
                            maxtime: int = 0) -> None:
    """ animates grid occulation over simulation time, for the specified population(s), or all populations """
    if maxtime == 0: maxtime = df["simtime"].max()
    if df["simtime"].min() > mintime: mintime = df["simtime"].min()
    
    fig = plt.figure()
    camera = Camera(fig)
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # create scatter plots for the desired population scenario
    if len(population)<1: 
        warning("population list empty or not provided at all for plt_grid_occupation() in stats.py (abm framework)")

    else:
        # add titles and labels
        plt.title(f"grid occupancy for populations: {str(population)}")
        plt.xlabel("columns")
        plt.ylabel("rows")

        if population[0] == "all":
            
            df = df[df["agents"] > 0]            
            for i in range(mintime, maxtime+1):
                
                # use "agents" column data from results database (pandas.DataFrame)
                fig.clf()
                subdf = df[df["simtime"] == i]
                plt.scatter(x = subdf["col"],
                            y = subdf["row"],
                            alpha = subdf["agents"]/df["agents"].max(),
                            c = color,
                            label = "all")
                
                if i == mintime: plt.legend()

                plt.pause(tpf)
                camera.snap()

        else:

            df = df[df["agents"] > 0]            
            for i in range(mintime, maxtime+1):

                fig.clf()

                subdf = df[df["simtime"] == i]
                
                for pop in population:

                    popdf = subdf[subdf[pop] > 0]
                    plt.scatter(x = popdf["col"],
                                y = popdf["row"],
                                alpha = popdf[pop] / popdf[pop].max,
                                c = color,
                                label = pop)
                
                if i == mintime: plt.legend()

                plt.pause(tpf)
                camera.snap()

        # build animation from data and save it
        animation = camera.animate()
        animation.save(config.path_saveanimations+"/"+filename+".gif", writer='PillowWriter', fps=int(1/tpf))