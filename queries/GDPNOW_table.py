import sqlite3
import pandas
from datetime import datetime


con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqlite")

def q_identifier(date):
    start_q = [1, 4, 7, 10]
    dt = datetime.strptime(date, '%Y-%m-%d')
    month = dt.month
    q = ((month-1)//3)+1
    if q in start_q:
        if dt.day < 7:
            if dt.weekday() > 4:    #If 1st day is in weekend
                if q > 1:
                    q = q-1
                else:
                    q = 4
    q_date = str(dt.year) + "-" + str(q)
    return q_date

df_gdpnow = pandas.read_sql_query(
    "SELECT DATE(Actual_Date_AGDPNO) AS DATE, Actual_AGDPNO FROM AGDPNO", con)
df_m2 = pandas.read_sql_query(
    "SELECT DATE(Actual_Date_FM2LW) AS DATE, Actual_FM2LW FROM FM2LW", con)
df_last_q_gdp = pandas.read_sql_query(
    "SELECT DATE(Actual_Date_FGDPQ) AS DATE, Actual_FGDPQ FROM FGDPQ LIMIT 1", con)

last_q_gdp = df_last_q_gdp.at[0, 'Actual_FGDPQ']
df_gdpnow['Actual_AGDPNO_lin'] = ((df_gdpnow['Actual_AGDPNO']/100)+1)*last_q_gdp


df_m2['Quarter'] = df_m2['DATE'].apply(lambda x: q_identifier(x))
current_q = df_m2.at[0, 'Quarter']
df_m2 = df_m2.loc[df_m2['Quarter'] == current_q]
df_m2["Q_avg_FM2LW"] = df_m2['Actual_FM2LW'].sort_values(ascending=True).expanding().mean()

#df_m2 = df_m2.groupby(['Quarter'])['Actual_FM2LW'].mean().reset_index(name='Average_FM2LW').sort_values(by=['Quarter'], ascending=False).reset_index(drop=True)

print(df_gdpnow)
#df.to_sql(name="GDPNOW_current_quarter", con=out)