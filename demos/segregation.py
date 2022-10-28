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
                        size = 50, 
                        attributes = attrs, 
                        datatypes = datatypes, 
                        initialvals = [100, "native"]
                        )
    pops.add_population(name = "immigrants",
                        size = 50,
                        attributes = attrs,
                        datatypes = datatypes,
                        initialvals = [100, "immigrant"]
                        )
    
    # setup simulation
    sim = framework.Simulation(1000)

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(sim.Iteration)
    pops.write_agents_to_db(sim.Iteration)
    
    agents = pops.get_agents()

    # other model specific global settings
    _max_search = 10
    _impactarea = 1

    # execute simulation run
    while sim.run():
        
        # select one random agent
        agent = random.choice(agents)

        # get that agents neighbourhood
        neighbours = env.get_neighbourhood(agent, mode = "moore", radius = _impactarea)

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
        cells = env.get_freecells(n = _max_search)

        for c in cells:
            
            util_new = 0.0

            neighbours = env.get_neighbourhood(c, "moore", radius = _impactarea)

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
        if (sim.Iteration % 10) == 0:
            pops.write_agents_to_db(sim.Iteration)
            pops.write_env_to_db(sim.Iteration)
            pops.write_density_to_db(sim.Iteration)
    
    # get dataframes with simulation results 
    agents_df = db_manager.get_agentsdf()
    env_df = db_manager.get_environmentdf()
    density_df = db_manager.get_densitydf()
    
    # visualize simulation data
    stats.set_fontsizes(8,10,12)

    stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=0, markersize = 150.0)
    stats.save_plot("segplt_early_ia1_50agents_1000it")

    stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=500, markersize = 150.0)
    stats.save_plot("segplt_intermediate_ia1_50agents_1000it")

    stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=1000, markersize = 150.0)
    stats.save_plot("segplt_late_ia1_50agents_1000it")

    stats.plot_avgattr_lines(["utility"], agents_df)
    stats.save_plot("avgutil_ia1_50agents_1000it")

    animation.animate_grid_occupation(
                            df = env_df,
                            filename = "segvid_ia1_50agents_1000it",
                            population = ["natives","immigrants"],
                            colors = ["#F52D2D","#4A87F1"],
                            tpf = 0.20, # time per frame
                            mintime = 0,
                            maxtime = 1000, 
                            markersize = 150.0
                        )

    animation.animate_density(
                            df = density_df,
                            filename = "segdens_ia1_50agents_1000it",
                            attr = "utility",
                            defaultsize = 150,
                            color = "#F52D2D",
                            tpf = 0.20,
                            maxtime = 1000
    )
    
    # end program
    db.close()
    print("demo ends")