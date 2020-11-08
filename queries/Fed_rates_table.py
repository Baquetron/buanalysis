import sqlite3
import pandas

con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqilte")

df = pandas.read_sql_query("", con)
print(df)

