import data
import stats
import config
import pandas
import animation

db = data.Database("sqlite3",config.path_databasefile)

density_df = pandas.read_sql_query("SELECT * FROM density", db.Connection)

stats.set_fontsizes(8,10,12)


animation.animate_density(
        df = density_df,
        filename = "goltest",
        attr = "life_t0",
        defaultsize = 50,
        color = "black",
        tpf = 0.10
    )

db.close()