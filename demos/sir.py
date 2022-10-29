
__author__ = "Linnart Felkl"
__email__ = "LinnartSF@gmail.com"

if __name__ == "__main__":

    print("demo starts")

    import sys
    from pathlib import Path
    file = Path(__file__).resolve()
    parent, root = file.parent, file.parents[1]
    sys.path.append(str(root))

    # remove the current file's directory from sys.path, unless already removed
    try:
        sys.path.remove(str(parent))
    except ValueError:
        pass

    import data
    import stats
    import config
    import framework
    import random
    import animation

    # setup database manager and connection
    db = data.Database("sqlite3", config.path_databasefile)
    db_manager = data.Manager(db)
    
    # create an empty environment
    env = framework.Environment(1, True, 20, 20, db_manager) # Environment constructor implicitly resets environment table in database

    # create initial population of healthy humans
    pops = framework.Populations(amount = 1, env = env, db_manager = db_manager, attributes = ["infected","recovered"], datatypes = ["INTEGER","INTEGER"])
    pops.add_population(name = "humans", 
                        size = 200, 
                        attributes = ["infected","recovered"], 
                        datatypes = ["INTEGER","INTEGER"], 
                        initialvals = [0, 0]
                        )

    # randomly infect 5%
    pop = pops.Populations["humans"]
    sampleagents = pop.get_agents(int(0.05*pop.Size))
    for agent in sampleagents: agent.Attributes["infected"] = 1

    _prob_infection = 0.07
    _prob_recovery = 0.03
    
    # setup simulation
    sim = framework.Simulation(300)

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(sim.Iteration)
    pops.write_agents_to_db(sim.Iteration)

    # execute simulation run, store every 10th run into the database
    while sim.run():

        # look at every agent
        for agent in pop.get_agents():
            if agent.get_attr_value("infected") == 1:
                
                neighbours = env.get_neighbourhood(agent)
                for neighbour in neighbours:
                    if neighbour.get_attr_value("infected") == 0 and neighbour.get_attr_value("recovered") == 0:
                        
                        # this neighbour is not resistant and not infected; infect with specified probability
                        if random.uniform(0, 1) < _prob_infection: neighbour.set_attr_value("infected", 1)
            
                # the infected agent recovers with a specified probability
                if random.uniform(0, 1) < _prob_recovery: 
                    agent.set_attr_value("recovered", 1)
                    agent.set_attr_value("infected", 0)
                
        # update results in database, for agents and for environment
        pops.write_agents_to_db(sim.Iteration)
        pops.write_env_to_db(sim.Iteration)
        pops.write_density_to_db(sim.Iteration)
    
    # get dataframes with simulation results 
    humans_df = db_manager.get_populationdf(pop = "humans")
    env_df = db_manager.get_environmentdf()
    density_df = db_manager.get_densitydf()
    
    # visualize simulation data
    stats.set_fontsizes(8,10,12)

    stats.plot_agentattr_lines("infected", humans_df)
    stats.save_plot("infection_curves")
    
    stats.plot_agentattr_lines("recovered", humans_df)
    stats.save_plot("recovery_curves")

    stats.plot_grid_occupation(env_df, ["humans"])
    stats.save_plot("human_locations")

    stats.plot_density_markersize(density_df, "infected", 50, "red")
    stats.save_plot("infection_density")

    stats.plot_density_markersize(density_df, "recovered", 50, "green")
    stats.save_plot("recovery_density")

    stats.plot_avgattr_lines(["recovered","infected"], humans_df)
    stats.save_plot("avginfectedavgrecovered")
    
    # create and save animations
    animation.animate_density(
        df = density_df,
        filename = "infectionanimation",
        attr = "infected",
        defaultsize = 50,
        color = "red",
        tpf = 0.05
    )
 
    animation.animate_density(
        df = density_df,
        filename = "recoveryanimation",
        attr = "recovered",
        defaultsize = 50,
        color = "green",
        tpf = 0.05
    )
    
    # end program
    db.close()
    print("demo ends")