import sqlite3
import pandas
from datetime import datetime


con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqlite")

def generator(con, a1, a2, a3, a4):
    df = pandas.read_sql_query(
        "SELECT DATE, Actual_FFFTULD, Actual_FFFTLLD, Actual_FEFFRM, Actual_AWXSFRM FROM (SELECT strftime('%Y-%m', Actual_Date_FFFTULD) AS DATE, Actual_FFFTULD, Actual_FFFTLLD FROM FFFTULD, FFFTLLD, AWXSFRM WHERE Actual_Date_FFFTULD = Actual_Date_FFFTLLD GROUP BY DATE ORDER BY DATE DESC), FEFFRM, AWXSFRM WHERE (DATE = Actual_Date_FEFFRM AND Actual_Date_FEFFRM = strftime('%Y-%m', Actual_Date_AWXSFRM))", con)

    df.to_sql(name="Fed_rates", con=out)


if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    a = "FFFTULD"
    arg1 = "FFFTLLD"
    arg2 = "FEFFRM"
    arg3 = "AWXSFRM"
    #simple_table_to_plot(con, out, a, arg1, arg2, arg3)
    generator(con, a, arg1, arg2, arg3)