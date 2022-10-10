
__author__ = "Linnart Felkl"
__email__ = "linnartsf@gmail.com"

if __name__ == "main":

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
    for i in range(0, 10):
        agent = framework.Agent(i, ["life"], [random.uniform(0,1)])
        env.add_agent(agent)
        agents.append(agent)

    # deleting all old records in database and reset to default format
    db_manager.reset_table("agents")

    # upate database columns in accordance with framework components used
    db_manager.add_agentcolumn("life","REAL")

    # test prints
    print(str(env))
    print(str(env.Array))
    print(agent.Attributes.keys())
    print(agent.Attributes.values())

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
            db_manager.write_agentvalue(iteration, agent)
        if iteration >= maxiteration:
            running = False
            break

    # before exiting script, close the database
    db.close()
