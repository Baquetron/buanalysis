import sqlite3
import pandas

con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqilte")

df = pandas.read_sql_query(
    "SELECT DATE(Actual_Date_FFFTULD) AS DATE, Actual_FFFTULD, Actual_FFFTLLD FROM FFFTULD, FFFTLLD WHERE Actual_Date_FFFTULD = Actual_Date_FFFTLLD", con)
#print(df)
df.to_sql(name="Fed_rates_table", con=out)

