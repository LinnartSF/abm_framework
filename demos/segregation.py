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
    attrs = ["utility","type"]
    datatypes = ["REAL","TEXT"]
    pops = framework.Populations(amount = 2, env = env, db_manager = db_manager, attributes = attrs, datatypes = datatypes)
    pops.add_population(name = "natives", 
                        size = 150, 
                        attributes = attrs, 
                        datatypes = datatypes, 
                        initialvals = [100, "native"]
                        )
    pops.add_population(name = "immigrants",
                        size = 150,
                        attributes = attrs,
                        datatypes = datatypes,
                        initialvals = [100, "immigrant"]
                        )
    
    # setup simulation
    sim = framework.Simulation(250)

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(sim.Iteration)
    pops.write_agents_to_db(sim.Iteration)
    
    agents = pops.get_agents()

    # other model specific global settings
    _max_search = 5

    # execute simulation run
    while sim.run():
        
        # select one random agent
        agent = random.choice(agents)

        # get that agents neighbourhood
        neighbours = env.get_neighbourhood(agent, mode = "moore", radius = 5)

        util_is = 0.0
        
        # if there are neighbours, then recalculate the utility of the agent
        for o in neighbours:
            
            if o.get_attr_value("type") == agent.get_attr_value("type"):

                util_is += 10
            
            else:

                util_is += -10
        
        # update agent utility 
        agent.increase_attr_value("utility",util_is)
        
        # for search up to maximum limit of random free cells to see if utility is better there
        cells = env.get_freecells(n = 5)

        for c in cells:
            
            util_new = 0.0

            neighbours = env.get_neighbourhood(c, "moore", radius = _max_search)

            for o in neighbours:

                if o.get_attr_value("type") == agent.get_attr_value("type"):
            
                    util_new += 10

                else:

                    util_new += -10
            
            if util_new > util_is:

                # relocate agent, then break loop
                env.relocate(agent, c)
                agent.increase_attr_value("utility",util_new)
                break
                
        # update results in database, for agents and for environment
        pops.write_agents_to_db(sim.Iteration)
        pops.write_env_to_db(sim.Iteration)
        pops.write_density_to_db(sim.Iteration)
    
    # get dataframes with simulation results 
    agents_df = db_manager.get_agentsdf(condition = "(simtime%5) == 0")
    env_df = db_manager.get_environmentdf(condition = "(simtime%5) == 0")
    density_df = db_manager.get_densitydf(condition = "(simtime%5) == 0")
    
    # visualize simulation data
    stats.set_fontsizes(8,10,12)

    stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=2, markersize = 100.0)
    stats.save_plot("segregationplot_early")

    stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=125, markersize = 100.0)
    stats.save_plot("segregationplot_intermediate")

    stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=250, markersize = 100.0)
    stats.save_plot("segregationplot_late")

    stats.plot_avgattr_lines(["utility"], agents_df)
    stats.save_plot("avgagentutility")

    animation.animate_grid_occupation(
                            df = env_df,
                            filename = "segregationvideo",
                            population = ["natives","immigrants"],
                            colors = ["#F52D2D","#4A87F1"],
                            tpf = 0.10, # time per frame
                            mintime = 0,
                            maxtime = 250, 
                            markersize = 150.0
                        )

    animation.animate_density(
                            df = density_df,
                            filename = "segregationutility",
                            attr = "utility",
                            defaultsize = 150,
                            color = "#F52D2D",
                            tpf = 0.10,
                            maxtime = 250
    )
    
    # end program
    db.close()
    print("demo ends")