import data
import stats
import config
import pandas
import animation

db = data.Database("sqlite3",config.path_databasefile)

env_df = pandas.read_sql_query("SELECT * FROM environment", db.Connection)
agents_df = pandas.read_sql_query("SELECT * FROM agents", db.Connection)

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

animation.animate_grid_occupation(env_df, 
                            "segregationvideo",
                            population = ["natives","immigrants"],
                            markersize = 120,
                            tpf = 0.10
                            )

db.close()