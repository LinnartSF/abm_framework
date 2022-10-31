import data
import stats
import config
import pandas
import animation

db = data.Database("sqlite3",config.path_databasefile)

density_df = pandas.read_sql_query("SELECT * FROM density", db.Connection)

print(density_df.head())
print(density_df.tail())

stats.set_fontsizes(8,10,12)


db.close()