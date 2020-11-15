import sqlite3
import pandas

con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqlite")

df = pandas.read_sql_query(
    "SELECT DATE(Actual_Date_AGDPNO) AS DATE, Actual_AGDPNO FROM AGDPNO", con)
#print(df)
df.to_sql(name="GDPNOW_current_quarter", con=out)