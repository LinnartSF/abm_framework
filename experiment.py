
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

    # deleting all old records in database and reset to default format
    db_manager.reset_table("agents")
    db_manager.reset_table("environment")

    # upate database columns in accordance with framework components used
    db_manager.add_agentcolumn("life","REAL") # TODO: transfer this into
    db_manager.add_environmentcolumns(["pop_a","pop_b"], ["INTEGER","INTEGER"])

    # place and create 10 agents of the same type onto the environment
    agents_a = []
    for i in range(0, 20):
        agent = framework.Agent(i, ["life"], [random.uniform(0,1)])
        env.add_agent(agent)
        agents_a.append(agent)
    agents_b = []
    for i in range(0, 20):
        agent = framework.Agent(i+19, ["life"], [random.uniform(0,1)])
        env.add_agent(agent)
        agents_b.append(agent)

    # setup simulation run
    iteration = 0
    for agent in agents_a:
        db_manager.write_agentvalue(iteration, agent)
        db_manager.write_environmentcell(iteration, agent.Row, agent.Col, env, [1, 0])
    for agent in agents_b:
        db_manager.write_agentvalue(iteration, agent)
        db_manager.write_environmentcell(iteration, agent.Row, agent.Col, env, [0, 1])

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