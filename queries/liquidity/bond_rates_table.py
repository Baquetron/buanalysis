import sqlite3
import pandas
from datetime import date
from datetime import timedelta
from datetime import datetime

def get_value(con, ticker, n_days, source='BDD'):
    df = pandas.read_sql_query("SELECT DATE(Actual_Date_"+ ticker +") AS DATE, Actual_"+ ticker +" FROM "+ ticker, con)
    last_day = datetime.strptime(df.at[0, "DATE"], '%Y-%m-%d')

    if n_days == 0:
        return df.at[0, "Actual_" + ticker]
    
    d_n_days = last_day.date()-timedelta(days=n_days)
    for i, elem in enumerate(df["DATE"]):
        dt = datetime.strptime(elem, '%Y-%m-%d').date()
        if dt <= d_n_days:
            return df.at[i, "Actual_" + ticker]

    return False

def generate_bonds_curve(con, out, to_sql=True):
    bond_list = {"30y":"F30YBD", "20y":"F20YBD", "10y":"F10YBD", "5y":"F5YBD", "2y":"F2YBD", "1y":"F1YBD", "6m":"F6MBD", "3m":"F3MBD", "1m":"F1MBD"}
    time_idx = {"Maturity":None, "Actual":0, "1y":365, "2y": 730}
    table = [list(time_idx.keys())]
    time_idx_loop = list(time_idx.keys())[1:]
    for i, elem in enumerate(bond_list.keys()):
        row = [elem]
        for j, tframe in enumerate(time_idx_loop):
            row.append(get_value(con, bond_list[elem], time_idx[tframe]))
        table.append(row)
    
    headers_df = table.pop(0)
    df_table = pandas.DataFrame(table, columns=headers_df)
    if to_sql == True:
        df_table.to_sql(name="Bond_yield_curve", con=out)
    else:
        print(df_table)

def generate_TIPS_table(con, out, to_sql=True):
    bond_list = {"30y":"F30Y", "20y":"F20Y", "10y":"F10Y"}
    time_idx = {"Maturity":None, "Bond":"BD", "Inflation-Indexed bond":"IBD"}
    table = [list(time_idx.keys())]
    time_idx_loop = list(time_idx.keys())[1:]
    for i, elem in enumerate(bond_list.keys()):
        row = [elem]
        for j, tframe in enumerate(time_idx_loop):
            row.append(get_value(con, bond_list[elem] + time_idx[tframe], 0))
        table.append(row)
    
    headers_df = table.pop(0)
    df_table = pandas.DataFrame(table, columns=headers_df)
    if to_sql == True:
        df_table.to_sql(name="Bond_TIPS_curve", con=out)
    else:
        print(df_table)

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")

    #generate_bonds_curve(con, out, False)
    generate_TIPS_table(con, out, False)