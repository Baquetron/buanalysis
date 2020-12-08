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
df_m2 = df_m2.drop(['Quarter'], axis=1)

df_vom2 = df_gdpnow.append(df_m2, ignore_index=True, sort=False) #Appends second df to end of 1st df
d = {'Actual_AGDPNO':'first', 'Actual_AGDPNO_lin':'first', 'Actual_FM2LW':'last', 'Q_avg_FM2LW':'last'}
df_vom2 = df_vom2.groupby('DATE', sort=False, as_index=False).agg(d) #Groups df taking 1st the att from 1st df
df_vom2 = df_vom2.sort_values(['DATE'], ascending=True).reset_index(drop=True)
df_vom2 = df_vom2.fillna(method="ffill").fillna(method="bfill")
df_vom2['Actual_VOM2'] = df_vom2['Actual_AGDPNO_lin']/df_vom2['Q_avg_FM2LW']

df_vom2.to_sql(name="GDPNow_vs_VoM2_current_quarter", con=out)