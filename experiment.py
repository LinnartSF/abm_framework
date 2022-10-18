
__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

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
                        datatypes = ["INTEGER","INTEGER"], 
                        initialvals = [100, 10], 
                        randomness = [["uniform",0.8,1.2], ["uniform",0.6,1.4]]) # TODO: replace randoness list by a custom datatype (Distribution class); add it to framework.py module
    pops.add_population(name = "customers", 
                        size = 20, 
                        attributes = ["demand"], 
                        datatypes = ["INTEGER"], 
                        initialvals=[50], 
                        randomness=[["uniform",0.5,1.5]])

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
            
            for agent in env.get_neighbourhood(customer, "moore", 3, "random"):
                if agent.Population == "producers":
                    if agent.get_attr_value("inventory") >= customer.get_attr_value("demand"):

                        agent.set_attr_value("inventory", 
                                             agent.get_attr_value("inventory") - customer.get_attr_value("demand"))
                        customer.set_attr_value("demand", 0)
                    
                    else:
                        customer.set_attr_value("demand", 
                                                customer.get_attr_value("demand") - agent.get_attr_value("inventory"))
            
        # update inventory values by produced amount
        for producer in pops.Populations["producers"].get_producers():
            producer.set_attr_value("inventory", 
                                    producer.get_attr_value("inventory") + producer.get_attr_value("prodcapacity"))
        
        # update results in database, for agents and for environment
        pops.write_env_to_db(iteration)
        pops.write_env_to_db(iteration)

    db.close()
    print("test complete")