import data
import stats
import config
import pandas
import animation

db = data.Database("sqlite3",config.path_databasefile)

env_df = pandas.read_sql_query("SELECT * FROM environment", db.Connection)
agents_df = pandas.read_sql_query("SELECT * FROM agents", db.Connection)
density_df = pandas.read_sql_query("SELECT * FROM density", db.Connection)

stats.set_fontsizes(8,10,12)
"""
stats.plot_grid_occupation(env_df, ["natives","immigrants"], maxtime=2, markersize = 100.0)
stats.save_plot("segregationplot_early")

stats.plot_grid_occupation(env_df, ["natives","immigrants"], maxtime=250, markersize = 100.0)
stats.save_plot("segregationplot_intermediate")

stats.plot_grid_occupation(env_df, ["natives","immigrants"], maxtime=500, markersize = 100.0)
stats.save_plot("segregationplot_late")

stats.plot_avgattr_lines(["utility"], agents_df)
stats.save_plot("avgagentutility")
"""

animation.animate_grid_occupation(
                            df = env_df,
                            filename = "segregationvideo",
                            population = ["natives","immigrants"],
                            color = "red",
                            tpf = 0.01, # time per frame
                            mintime = 0,
                            maxtime = 20, 
                            markersize = 150.0
                        )
"""
animation.animate_density(
        df = density_df,
        filename = "segregationutility2",
        attr = "utility",
        defaultsize = 150,
        color = "red",
        tpf = 0.01
    )
"""
db.close()