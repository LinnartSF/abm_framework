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
    attrs = ["purchased"]
    datatypes = ["INTEGER"]
    pops = framework.Populations(amount = 1, env = env, db_manager = db_manager, attributes = attrs, datatypes = datatypes)
    pops.add_population(name = "customers", 
                        size = 100, 
                        attributes = attrs, 
                        datatypes = datatypes, 
                        initialvals = [0]
                        )
    
    # model specific global settings (parameter values)
    _prob_recommend = 0.1
    _impactarea = 3
    _initialclients = 5

    # setup simulation
    sim = framework.Simulation(50)

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(sim.Iteration)
    pops.write_agents_to_db(sim.Iteration)
    
    agents = pops.get_agents()

    # set 5 initial purchases 
    for _ in range(_initialclients):
        agent = random.choice(agents)
        agent.set_attr_value("purchased", 1)

    # execute simulation run; with centralized simulation control
    while sim.run():
        
        # select one random agent after the other
        random.shuffle(agents)
        for agent in agents:

            # get that agents neighbourhood
            neighbours = env.get_neighbourhood(agent, mode = "moore", radius = _impactarea)

            for neighbour in neighbours:
                
                if agent.get_attr_value("purchased") == 1 and neighbour.get_attr_value("purchased") == 0 and random.uniform(0,1) < _prob_recommend: neighbour.set_attr_value("purchased", 1)

                if agent.get_attr_value("purchased") == 0 and neighbour.get_attr_value("purchased") == 1 and random.uniform(0,1) < _prob_recommend: 
                    
                    agent.set_attr_value("purchasd", 1)
                    break               
                
        # update results in database, for agents and for environment
        pops.write_agents_to_db(sim.Iteration)
    
    # get dataframes with simulation results 
    agents_df = db_manager.get_agentsdf()
    
    # visualize simulation data
    stats.set_fontsizes(8,10,12)

    stats.plot_avgattr_lines(["purchased"], agents_df)
    stats.save_plot("avgpurchasingshare")

    # end program
    db.close()
    print("demo ends")