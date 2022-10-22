""" 

This module is used for visualizing results generated by the ABM simulation runs. 

The standardized results, stored in the database, are visualized using matplotlib.pyplot, which is wrapped by this module. The module also makes use of pandas.

The module provides a set of pre-defined plotting functions. Data is forwarded to these in the form of input arguments. The functions then create the plots. 
Functionality is also provided for saving plots as pdf or png. Destination directory must be specified in the config-file. Alternatively, paths where plots are saved can be specified as input arguments. 

"""

__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

import data
import config
from matplotlib import pyplot as plt
import pandas
from matplotlib.ticker import MaxNLocator

plt.style.use("fivethirtyeight")

def warning(msg: str) -> None:
    """ helper function that prints a warning into console; used when invalid input is forwarded to one of the functions in the module """
    print(f"WARING: {msg}")

def set_plotstyle(style: str) -> None:
    """ sets matplotlib plotstyle """
    plt.style.use(style)

def set_fontsizes(smallsize: float, mediumsize: float, largesize: float):
    """ function for setting font size standard for all plotting functions in module """
    plt.rc('font', size = smallsize)          # controls default text sizes
    plt.rc('axes', titlesize = smallsize)     # fontsize of the axes title
    plt.rc('axes', labelsize = mediumsize)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize = smallsize)    # fontsize of the tick labels
    plt.rc('ytick', labelsize = smallsize)    # fontsize of the tick labels
    plt.rc('legend', fontsize = smallsize)    # legend fontsize
    plt.rc('figure', titlesize = largesize)   # fontsize of the figure title

def set_edgecolor(color: str) -> None:
    """ sets edge color of all plots in this module """
    plt.rcParams["axes.edgecolor"] = color

def set_autolayout(autolayout: bool) -> None:
    """ sets autolayout True or False for all plotting functions in this module """
    plt.rcParams["figure.autolayout"] = autolayout

def set_linewidth(linewidth: float) -> None:
    """ sets axes linewidth for all plotting functions in this module """
    plt.rcParams["axes.linewidth"] = linewidth

def set_figsize(w: float, 
                h: float) -> None:
    """ sets fig size for entire plotting module """
    plt.rcParams["figure.figsize"] = [w, h]

def save_plot(filename: str, filepath: str = "") -> None:
    """ stores plot as png and pdf, for specified equipment name """
    if filepath == "": filepath = config.path_saveplots
    plt.savefig(filepath+"\\"+filename+".png")
    plt.savefig(filepath+"\\"+filename+".pdf")

def plot_agentattr_line(agent_id: int, 
                        attr: str,
                        df: pandas.DataFrame,
                        mintime: int = 0,
                        maxtime: int = 0) -> None:
    """ creates a line plot for for individual agent attribute value, for a single agent, throughout time (for one attribute) """
    
    # derive relevant plotting data
    df = df[df["id"] == agent_id]
    x = df["simtime"]
    y = df[attr]

    # create new figure
    plt.figure()

    # create plot 
    plt.plot(x, 
             y,
             label = attr,
             linewidth = 1.0)
    
    # set axis limits, if relevant
    if maxtime > 0:
        plt.xlim(mintime, maxtime)

    # set titles
    plt.title(f"{attr} for agent {str(agent_id)} over time")
    plt.xlabel("simulation time")
    plt.ylabel(attr)

    # add legend
    plt.legend()

# TODO further specify this function to allow to sample a subset of agents randomly
def plot_agentattr_lines(attr: str,
                         df: pandas.DataFrame,
                         mintime: int = 0,
                         maxtime: int = 0) -> None:
    """ plots trajectories for all agents in dataset, but only for the specified attribute """
    
    # unique list of agents; for each agent one line will be added to the plot
    ids = df["id"].unique()

    # create new figure
    plt.figure()

    # create a line plot for each agent
    for id in ids:
        subset = df[df["id"] == id]
        plt.plot(subset["simtime"], 
                 subset[attr],
                 label = str(id),
                 linewidth=1.0)
    
    # set axis limits, if relevant
    if maxtime > 0:
        plt.xlim(mintime, maxtime)
    
    # set titles
    plt.title(f"{attr} for agents throughput simulation time")
    plt.xlabel("simulation time")
    plt.ylabel(attr) 

    # add legend
    plt.legend()

def plot_avgattr_lines(attributes: list,
                       df: pandas.DataFrame,
                       mintime: int = 0,
                       maxtime: int = 0) -> None:
    """ plot avg value trajectory for all agents throughout time, for arbitrary amount of attributes """
    
    # calculate data to plot
    results = df.groupby("simtime").mean()

    # create new figure
    plt.figure()

    # for each attribute create a plot
    for attr in attributes:
        plt.plot(results.index, 
                 results[attr],
                 label = attr)
    
    # cut axis if relevant
    if maxtime > 0:
        plt.xlim(mintime, maxtime)
    
    # add titles
    plt.title("avg agent attribute value developments")
    plt.xlabel("simulation time")
    plt.ylabel("attribute values")

    # add legend
    plt.legend()

def plt_valdistribution(attributes: list,
                        df: pandas.DataFrame,
                        mintime: int = 0,
                        maxtime: int = 0) -> None:
    """ function for plotting dynamic relative state distribution among the state listed in attributes argument """

    # calculate plotting data
    results = df.groupby("simtime").sum()[attributes]
    results["total"] = results.sum(axis = 1)

    # create new figure
    plt.figure()

    # for each time index, create a stacked barplot
    y_old = None
    for attr in attributes:
        if y_old == None:
            plt.bar(results["simtime"], 
                     results[attr]/results["total"], 
                     label = attr)
            y_old = results[attr]/results["total"]
        else:
            plt.bar(results["simtime"], 
                     results[attr], 
                     bottom = y_old,
                     label = attr)
            y_old = y_old + results[attr]/results["total"]

    # cut axis if relevant
    if maxtime > 0:
        plt.xlim(mintime, maxtime)
    
    # add titles
    plt.title("dynamic relative state distribution of agents")
    plt.xlabel("simulation time")
    plt.ylabel("relative state distribution")

    # add legends
    plt.legend()

def plot_grid_occupation(df: pandas.DataFrame,
                         population: list = ["all"],
                         color: str = "red",
                         maxtime: int = 0) -> None:
    """ plot grid cell occupation (at least one agent in cell, or none), for "all" agent types or just for one or several agent types (i.e. "population") """

    # subset relevant data from the dataframe provided as argument
    if maxtime == 0: maxtime = df["simtime"].max()
    df = df[df["simtime"] == maxtime]

    # create new figure
    fig = plt.figure()
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # create scatter plots for the desired population scenari
    if len(population)<1: 
        warning("population list empty or not provided at all for plt_grid_occupation() in stats.py (abm framework)")
    else:
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
                            label = pop)

        # add titles
        plt.title(f"grid occupancy for populations: {str(population)}")
        plt.xlabel("columns")
        plt.ylabel("rows")

        # add legend
        plt.legend()

def plot_density_alpha(df: pandas.DataFrame,
                      attr: str,
                      color: str = "red",
                      maxtime: int = 0) -> None:
    """ function for plotting the density of specified attribute on a grid plot """

    # subset relevant data from the dataframe provided as argument
    if maxtime == 0: maxtime = df["simtime"].max()
    df = df[df["simtime"] == maxtime]

    # create new figure
    fig = plt.figure()
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # use attr column data from results database (pandas DataFrame)
    plt.scatter(df[df[attr]>0]["col"],
                df[df[attr]>0]["row"],
                alpha = df[df[attr]>0][attr]/df[attr].max(),
                c = color,
                label = attr)

    # add attributes
    plt.title(f"density grid for attr: {attr}")
    plt.xlabel("columns")
    plt.ylabel("rows")

    # add legend
    plt.legend()

def plot_density_markersize(df: pandas.DataFrame,
                      attr: str,
                      defaultsize: float,
                      color: str = "red",
                      maxtime: int = 0) -> None:
    """ function for plotting the density of specified attribute on a grid plot """

    # subset relevant data from the dataframe provided as argument
    if maxtime == 0: maxtime = df["simtime"].max()
    df = df[df["simtime"] == maxtime]

    # create new figure
    fig = plt.figure()
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    # use attr column data from results database (pandas DataFrame)
    plt.scatter(df[df[attr]>0]["col"],
                df[df[attr]>0]["row"],
                s = defaultsize*(df[df[attr]>0][attr]/df[attr].max()),
                c = color,
                label = attr)

    # add attributes
    plt.title(f"density grid for attr: {attr}")
    plt.xlabel("columns")
    plt.ylabel("rows")

    # add legend
    plt.legend()
