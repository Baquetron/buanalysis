import pandas
import sqlite3

def generate(con, out):
    df_pmi = pandas.read_sql_query("SELECT Actual_Date_IPMICMM AS DATE, Actual_IPMICMM, Actual_IPMIMM, Actual_IPMISM, Release_Date_IPMICMM, Release_Date_IPMIMM, Release_Date_IPMISM FROM IPMICMM, IPMIMM, IPMISM WHERE (DATE=Actual_Date_IPMIMM AND DATE=Actual_Date_IPMISM) ORDER BY Release_Date_IPMICMM DESC LIMIT 13", con)

    df_pmi.to_sql(name="PMI_Markit_forecast", con=out)

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    generate(con, out)