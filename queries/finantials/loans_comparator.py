import sqlite3
import pandas

def generate(con, out, name="CI_loans_by_year", a1="FCILACBPCHM"):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +" FROM "+ a1, con)

    actual_12m = df.loc[0:11, "Actual_"+ a1]
    list_1y = df.loc[12:23, "Actual_"+ a1]
    df["1y"] = pandas.DataFrame(list_1y).reset_index(drop=True).rename(columns={"Actual_"+ a1: "1y"})
    list_2y = df.loc[24:35, "Actual_"+ a1]
    df["2y"] = pandas.DataFrame(list_2y).reset_index(drop=True).rename(columns={"Actual_"+ a1: "2y"})
    df = df.loc[0:11]

    df.to_sql(con=out, name=name, if_exists='replace')

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    generate(con, out)
