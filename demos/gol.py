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

    import time
    starttime = time.time()

    # setup database manager and connection
    db = data.Database("sqlite3", config.path_databasefile)
    db_manager = data.Manager(db)
    
    # create an empty environment
    env = framework.Environment(1, False, 10, 10, db_manager) # Environment constructor implicitly resets environment table in database

    # create initial population of healthy humans
    attrs = ["life_t0","life_t1"]
    datatypes = ["INTEGER","INTEGER"]
    pops = framework.Populations(amount = 1, env = env, db_manager = db_manager, attributes = attrs, datatypes = datatypes)
    pops.add_population(name = "units", 
                        size = 100, 
                        attributes = attrs, 
                        datatypes = datatypes, 
                        initialvals = [0, 0]
                        )
   
    # set seed of simulation (number of agents alive and their pattern)
    agents = pops.get_agents()
    random.shuffle(agents)
    for i in range(50):
        agents[i].set_attr_value("life_t0",1)

    # setup simulation
    sim = framework.Simulation(100)

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(sim.Iteration)
    pops.write_agents_to_db(sim.Iteration)

    # execute simulation run; with centralized simulation control
    while sim.run():
        
        for agent in agents:

            # get that agents neighbourhood
            neighbours = env.get_neighbourhood(agent, mode = "moore", radius = 1)

            _neighbours_alive = 0
            for neighbour in neighbours:
                
                if neighbour.get_attr_value("life_t0") == 1: 
                    _neighbours_alive  += 1

            if agent.get_attr_value("life_t0") == 1: 

                if _neighbours_alive == 2 or _neighbours_alive == 3: 
                    
                    agent.set_attr_value("life_t1", 1)

                else:

                    agent.set_attr_value("life_t1", 0)

            elif _neighbours_alive == 3:

                agent.set_attr_value("life_t1", 1)

            else:

                agent.set_attr_value("life_t1", 0)
                
        # update results in database, for agents and for environment
        pops.write_agents_to_db(sim.Iteration)
        pops.write_density_to_db(sim.Iteration)

        # update attributes for next round
        for agent in agents:

            agent.set_attr_value("life_t0", agent.get_attr_value("life_t1"))
    
    # get dataframes with simulation results
    density_df = db_manager.get_densitydf()

    # visualize simulation data
    stats.set_fontsizes(8,10,12)

    animation.animate_density(
        df = density_df,
        filename = "gol_randombounded",
        attr = "life_t1",
        defaultsize = 50,
        color = "black",
        tpf = 0.30
    )

    # end program
    db.close()
    print("demo ends")

    endtime = time.time()
    print(str(endtime-starttime))