import sqlite3
import pandas

con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqlite")

df = pandas.read_sql_query(
    "SELECT DATE(Actual_Date_FFFTULD) AS DATE, Actual_FFFTULD, Actual_FFFTLLD, Actual_FEFFRM, Actual_AWXSFRM FROM FFFTULD, FFFTLLD, FEFFRM, AWXSFRM WHERE (Actual_Date_FFFTULD = Actual_Date_FFFTLLD AND Actual_Date_FFFTLLD = Actual_Date_FEFFRM AND Actual_Date_FEFFRM = Actual_Date_AWXSFRM)", con)
#print(df)
df.to_sql(name="Fed_rates", con=out)

