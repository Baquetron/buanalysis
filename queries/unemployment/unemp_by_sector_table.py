import sqlite3
import pandas

NUM_ROWS = "13"   # Num of rows to display in plot

def generator(con, out, name,  a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +", Actual_"+ a2 +", Actual_"+ a3 +", Actual_"+ a4 +", Actual_"+ a5 + ", Actual_"+ a6 + ", Actual_"+ a7 + ", Actual_"+ a8 + ", Actual_"+ a9 + ", Actual_"+ a10 + ", Actual_"+ a11 +" FROM "+ a1 +", "+ a2 +", "+ a3 +", "+ a4 +", "+ a5 + ", "+ a6 +", "+ a7 +", "+ a8 +", "+ a9 +", "+ a10 +", "+ a11 +" WHERE (Actual_Date_"+ a1 +" = Actual_Date_"+ a2 +" AND Actual_Date_"+ a2 +" = Actual_Date_"+ a3 +" AND Actual_Date_"+ a3 +" = Actual_Date_"+ a4 +" AND Actual_Date_"+ a4 +" = Actual_Date_"+ a5 +" AND Actual_Date_"+ a5 +" = Actual_Date_"+ a6 +" AND Actual_Date_"+ a6 +" = Actual_Date_"+ a7 +" AND Actual_Date_"+ a7 +" = Actual_Date_"+ a8 +" AND Actual_Date_"+ a8 +" = Actual_Date_"+ a9 +" AND Actual_Date_"+ a9 +" = Actual_Date_"+ a10 +" AND Actual_Date_"+ a10 +" = Actual_Date_"+ a11 +") LIMIT "+ NUM_ROWS, con)
    
    df.to_sql(name=name, con=out, if_exists='replace')

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    generator(con, out, "Unemployment_by_sector", "FURMQOM", "FURCM", "FURDGM", "FURNDGM", "FURMWRM", "FURTUM", "FURIM", "FURFAM", "FURPBSM", "FUREHM", "FURLHM")