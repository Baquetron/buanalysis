from datetime import date
from datetime import timedelta
from datetime import datetime
import pandas
import pandas_datareader as pdr
import sqlite3

def get_pch(ticker, n_days, source='yahoo'):
    today = date.today()
    weekday = today.weekday()
    if weekday > 4:
        n_days = weekday - 4
        today = today-timedelta(days=n_days)
    i_today = pdr.DataReader(ticker, data_source=source, start=today, end=today)["Close"][0]
    if n_days == 0:
        return i_today
    elif n_days == "ytd":
        d_n_days = str(today)[0:4]+"-01-01"
    else:
        d_n_days = today-timedelta(days=n_days)

    i_pch = ((i_today / pdr.DataReader(ticker,data_source=source, start=d_n_days)["Adj Close"][0]) - 1)*100

    return i_pch

def generate(out):
    headers = {"Time":None, "SP500":"^GSPC", "Dow Jones":"^DJI", "Nasdaq":"^IXIC", "5YB":"^FVX", "10YB":"^TNX", "30YB":"^TYX", "Gold":"GC=F", " Bitcoin":"BTC-USD"}
    time_idx = {"Today":0,"Week":7,"Month":30,"3Month":90,"6Month":180,"1Y":365, "YTD":"ytd"}
    table = [list(headers.keys())]
    headers_loop = list(headers.keys())[1:]
    for i, tframe in enumerate(time_idx.keys()):
        row = [tframe]
        for j, elem in enumerate(headers_loop):
            row.append(get_pch(headers[elem], time_idx[tframe]))
        table.append(row)
    
    headers_df = table.pop(0)
    df_table = pandas.DataFrame(table, columns=headers_df)
    df_table.to_sql(name="Indeces_table", con=out, if_exists='replace')




if __name__ == "__main__":
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    generate(out)
