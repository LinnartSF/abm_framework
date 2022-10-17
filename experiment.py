
__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

from unittest import runner


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

        customers = random.shuffle(pops.Populations["customers"].get_agents())
        for customer in customers:
            
            for agent in env.get_neighbourhood(customer, "moore", 3):
                if agent.Population == "producers":
                    if agent.get_attr_value("inventory") > 0:
                        # TODO proceed with implementing production economy example










    db.close()
    print("test complete")

    """ 
    # execute simulation run
    running = True
    maxiteration = 100
    while running:
        iteration += 1
        for agent in agents_a:
            oldval =  agent.get_attr_value("life")
            agent.set_attr_value("life", oldval + oldval*random.uniform(-0.02,0.1))
            db_manager.write_agentvalue(iteration, agent)
        if iteration >= maxiteration:
            running = False
            break
    
    # get agent data
    agentdf = db_manager.get_agentsdf()

    # configure plotting function
    stats.set_fontsizes(8, 10, 12)
    stats.set_edgecolor("black")
    stats.set_linewidth(1.0)

    # create life score trajectory line plot for all agents in dataframe
    stats.plot_avgattr_lines(["life"], agentdf)
    stats.save_plot("avglifeplot")

    stats.plot_agentattr_line(6, "life", agentdf)
    stats.save_plot("lifeplot6")

    stats.plot_agentattr_lines("life", agentdf)
    stats.save_plot("lifeplot")

    envdf = db_manager.get_environmentdf()

    stats.plot_grid_occupation(envdf, ["pop_a","pop_b"])
    stats.save_plot("occupation_pops")

    stats.plot_grid_occupation(envdf)
    stats.save_plot("occupation_agets")

    # before exiting script, close database
    db.close()

    print("test ends")
    """