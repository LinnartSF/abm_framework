
__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

from cProfile import run
from tokenize import Funny


if __name__ == "__main__":

    print("test starts")

    import data
    import stats
    import config
    import framework
    import random

    # setup database connection and manager 
    db = data.Database("sqlite3", config.path_databasefile)
    db_manager = data.Manager(db)

    # create an empty environment
    env = framework.Environment(1, True, 20, 20, db_manager) # Environment constructor implicitly resets environment table in database

    # create agent populations
    pops = framework.Populations(amount = 2, env = env, db_manager = db_manager)
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

    # make sure that environment and agents tables in database are setup at this time
    pops.write_env_to_db(0)
    pops.write_agents_to_db(0)

    # execute simulation
    # TODO: define framework for setting up a simulation run (class of some kind)
    running = True
    iteration = 0
    maxiteration = 100

    while running: 
        iteration +=1

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
        pops.write_agents_to_db(iteration)
        pops.write_env_to_db(iteration)

        if iteration >= maxiteration:
            running = False

    # get dataframes with simulation results 
    customer_df = db_manager.get_populationdf(pop = "customers")
    producer_df = db_manager.get_populationdf(pop = "producers")
    env_df = db_manager.get_environmentdf()
    
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

    # TODO: implement environment plot that plots attribute values in the form of scatter plot transparency or scatter plot size
    
    # end program
    db.close()
    print("test complete")