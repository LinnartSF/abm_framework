import data
import stats
import config
import pandas
import animation

db = data.Database("sqlite3",config.path_databasefile)

env_df = pandas.read_sql_query("SELECT * FROM environment WHERE (simtime%5) == 0", db.Connection)
agents_df = pandas.read_sql_query("SELECT * FROM agents WHERE (simtime%5) == 0 AND simtime <= 250", db.Connection)
density_df = pandas.read_sql_query("SELECT * FROM density WHERE (simtime%5) == 0", db.Connection)


stats.set_fontsizes(8,10,12)

stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=5, markersize = 150.0)
stats.save_plot("segregationplot_early")

stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=125, markersize = 150.0)
stats.save_plot("segregationplot_intermediate")

stats.plot_grid_occupation(env_df, ["natives","immigrants"], colors = ["#F52D2D","#4A87F1"], maxtime=250, markersize = 150.0)
stats.save_plot("segregationplot_late")

stats.plot_avgattr_lines(["utility"], agents_df)
stats.save_plot("avgagentutility")

""""
animation.animate_grid_occupation(
                            df = env_df,
                            filename = "segregationvideo",
                            population = ["natives","immigrants"],
                            colors = ["#F52D2D","#4A87F1"],
                            tpf = 0.10, # time per frame
                            mintime = 0,
                            maxtime = 250, 
                            markersize = 150.0
                        )

animation.animate_density(
        df = density_df,
        filename = "segregationutility",
        attr = "utility",
        defaultsize = 150,
        color = "#F52D2D",
        tpf = 0.10,
        maxtime = 250
    )
"""
db.close()