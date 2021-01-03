import sqlite3
import pandas
from datetime import datetime

NUM_ROWS = "24"   # Num of rows to display in plot

con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqlite")

def generator(con, out):
    df = pandas.read_sql_query(
        "SELECT DATE, Actual_FFFTULD, Actual_FFFTLLD, Actual_FEFFRM, Actual_AWXSFRM FROM (SELECT strftime('%Y-%m', Actual_Date_FFFTULD) AS DATE, Actual_FFFTULD, Actual_FFFTLLD FROM FFFTULD, FFFTLLD, AWXSFRM WHERE Actual_Date_FFFTULD = Actual_Date_FFFTLLD GROUP BY DATE ORDER BY DATE DESC), FEFFRM, AWXSFRM WHERE (DATE = Actual_Date_FEFFRM AND Actual_Date_FEFFRM = strftime('%Y-%m', Actual_Date_AWXSFRM)) LIMIT "+ NUM_ROWS, con)

    df.to_sql(name="Fed_rates", con=out, if_exists='replace')


if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    a = "FFFTULD"
    arg1 = "FFFTLLD"
    arg2 = "FEFFRM"
    arg3 = "AWXSFRM"
    generator(con, out)