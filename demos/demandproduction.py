
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

    # create agent populations
    pops = framework.Populations(amount = 2, env = env, db_manager = db_manager, attributes = ["inventory","prodcapacity","demand","hunger"], datatypes = ["REAL","REAL","REAL","REAL"])
    pops.add_population(name = "producers", 
                        size = 20, 
                        attributes = ["inventory","prodcapacity"], 
                        datatypes = ["REAL","REAL"], 
                        initialvals = [50, 10], 
                        randomness = [["uniform",0.8,1.2], ["uniform",0.6,1.4]]) # TODO: replace randoness list by a custom datatype (Distribution class); add it to framework.py module
    pops.add_population(name = "customers", 
                        size = 20,
                        attributes = ["demand","hunger"], 
                        datatypes = ["REAL","REAL"], 
                        initialvals=[50,10], 
                        randomness=[["uniform",0.5,1.5], ["uniform",0.6,1.4]])

    # setup simulation
    sim = framework.Simulation(100)

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(sim.Iteration)
    pops.write_agents_to_db(sim.Iteration)

    # execute simulation run
    while sim.Running: 
        sim.increment_iteration()

        # let every customer try to satisfy its demand
        customers = pops.Populations["customers"].get_agents()
        random.shuffle(customers)
        for customer in customers:
            
            for agent in env.get_neighbourhood(customer, "moore", 5, "random"):
                if agent.Population == "producers":
                    if agent.get_attr_value("inventory") >= customer.get_attr_value("demand"):

                        agent.set_attr_value("inventory", 
                                             agent.get_attr_value("inventory") - customer.get_attr_value("demand"))
                        customer.set_attr_value("demand", 0)
                    
                    else:
                        customer.set_attr_value("demand", 
                                                customer.get_attr_value("demand") - agent.get_attr_value("inventory"))
            
            customer.set_attr_value("demand", 
                                    customer.get_attr_value("demand") + customer.get_attr_value("hunger"))
            
        # update inventory values by produced amount
        for producer in pops.Populations["producers"].get_agents():
            producer.set_attr_value("inventory", 
                                    producer.get_attr_value("inventory") + producer.get_attr_value("prodcapacity"))
        
        # update results in database, for agents and for environment
        pops.write_agents_to_db(sim.Iteration)
        pops.write_env_to_db(sim.Iteration)
        pops.write_density_to_db(sim.Iteration)

    # get dataframes with simulation results 
    customer_df = db_manager.get_populationdf(pop = "customers")
    producer_df = db_manager.get_populationdf(pop = "producers")
    env_df = db_manager.get_environmentdf()
    density_df = db_manager.get_densitydf()
    
    # visualize simulation data
    stats.set_fontsizes(8,10,12)

    stats.plot_agentattr_lines("demand", customer_df)
    stats.save_plot("demandcurves")
    
    stats.plot_agentattr_lines("inventory", producer_df)
    stats.save_plot("inventorycurves")

    stats.plot_grid_occupation(env_df)
    stats.save_plot("all populations")

    stats.plot_grid_occupation(env_df, ["customers"])
    stats.save_plot("customer_locations")
    
    stats.plot_grid_occupation(env_df, ["producers"])
    stats.save_plot("producer_locations")

    stats.plot_avgattr_lines(["demand", "hunger"], customer_df)
    stats.save_plot("customer_avgattrs")

    stats.plot_density_alpha(density_df, "demand")
    stats.save_plot("customer_demanddensity")

    stats.plot_density_alpha(density_df, "inventory")
    stats.save_plot("customer_inventorydensity")

    stats.plot_density_markersize(density_df, "demand", 100)
    stats.save_plot("customer_demandsize")

    stats.plot_density_markersize(density_df, "inventory", 100)
    stats.save_plot("producer_inventorysize")

    # create and save animations
    animation.animate_density(
        df = density_df,
        filename = "inventoryanimation",
        attr = "inventory",
        defaultsize = 50,
        color = "red",
        tpf = 0.5
    )

    animation.animate_density(
        df = density_df,
        filename = "demandanimation",
        attr = "demand",
        defaultsize = 50,
        color = "red",
        tpf = 0.5
    )

    # end program
    db.close()
    print("demo ends")