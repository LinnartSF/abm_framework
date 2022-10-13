
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
    env = framework.Environment(1, True, 20, 20)

    # place and create 10 agents of the same type onto the environment
    agents = []
    for i in range(0, 3):
        agent = framework.Agent(i, ["life"], [random.uniform(0,1)])
        env.add_agent(agent)
        agents.append(agent)

    # deleting all old records in database and reset to default format
    db_manager.reset_table("agents")

    # upate database columns in accordance with framework components used
    db_manager.add_agentcolumn("life","REAL")

    # setup simulation run
    iteration = 0
    for agent in agents:
        db_manager.write_agentvalue(iteration, agent)

    # execute simulation runs
    running = True
    maxiteration = 100
    while running:
        iteration += 1
        for agent in agents:
            oldval =  agent.get_attr_value("life")
            agent.set_attr_value("life", oldval + oldval*random.uniform(-0.02,0.1))
            db_manager.write_agentvalue(iteration, agent)
        if iteration >= maxiteration:
            running = False
            break
    
    # get agent data
    agentdf = db_manager.get_agentsdf()

    # configure plotting formats
    stats.set_fontsizes(8,10,12)

    # create life score trajectory line plot for all agents in dataframe
    stats.plot_avgattr_lines(["life"], 
                               agentdf)
    stats.save_plot("avglifeplot")

    stats.plot_agentattr_lines("life", 
                               agentdf)
    stats.save_plot("lifeplot")

    # before exiting script, close database
    db.close()

    print("test ends")