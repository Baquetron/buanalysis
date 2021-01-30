import sqlite3
import pandas
from datetime import datetime

NUM_ROWS = "26"   # Num of rows to display in plot

def q_identifier_m(date):
        dt = datetime.strptime(date, '%Y-%m')
        month = dt.month
        if 1 < month <= 4:
            q = 1
        elif 4 < month <= 7:
            q = 2
        elif 7 < month <= 10:
            q = 3
        else:
            q = 4
        q_date = str(dt.year) + "-" + str(q)
        return q_date


def one_line_table(con, a1):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +" FROM "+ a1 +" LIMIT "+ NUM_ROWS, con)
    return df

def generate(con, out, name, a1, a2):
    df_loan = one_line_table(con, a1)
    df_loan["DATE"] = df_loan["DATE"].apply(lambda x: q_identifier_m(x))
    df_del = one_line_table(con, a2)

    df = pandas.merge(left=df_loan, right=df_del, on="DATE")
    df["DATE"] = df["DATE"].apply(lambda x: x.replace("-", "-0"))
    df.to_sql(con=out, name=name, if_exists='replace')


if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    generate(con, out, "CI_loans_vs_delinquency_rate", "FCILACBPCHQ", "GCIDRQ")