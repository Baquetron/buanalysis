import sqlite3
import pandas
from datetime import datetime


con = sqlite3.connect("data/db/economic_data.sqlite")
out = sqlite3.connect("data/db/dashboard_data.sqlite")

class cvo2m_tables:
    def sql_tables_importer(self):
        self.df_gdpnow = pandas.read_sql_query(
            "SELECT DATE(Actual_Date_AGDPNO) AS DATE, Actual_AGDPNO FROM AGDPNO", self.con)
        self.df_m2 = pandas.read_sql_query(
            "SELECT DATE(Actual_Date_FM2LW) AS DATE, Actual_FM2LW FROM FM2LW", self.con)
        self.df_vom2 = pandas.read_sql_query(
            "SELECT Actual_Date_FVM2 AS DATE, Actual_FVM2 FROM FVM2", self.con)
        self.df_gdpnowq = pandas.read_sql_query(
            "SELECT Actual_Date_FGDPNQ AS DATE, Actual_FGDPNQ FROM FGDPNQ", self.con)

    def __init__(self, con, out): 
        self.con = con
        self.out = out
        self.sql_tables_importer()

    def q_identifier_m(self, date):
        dt = datetime.strptime(date, '%Y-%m')
        month = dt.month
        q = ((month-1)//3)+1
        q_date = str(dt.year) + "-" + str(q)
        return q_date

    def q_identifier_d(self, date):
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

    def vom2now_table(self, w_sql=1):
        df_last_q_gdp = pandas.read_sql_query(
            "SELECT DATE(Actual_Date_FGDPQ) AS DATE, Actual_FGDPQ FROM FGDPQ LIMIT 1", self.con)
        last_q_gdp = df_last_q_gdp.at[0, 'Actual_FGDPQ']
        self.df_gdpnow['Actual_AGDPNO_lin'] = ((self.df_gdpnow['Actual_AGDPNO']/100)+1)*last_q_gdp

        self.df_m2['Quarter'] = self.df_m2['DATE'].apply(lambda x: self.q_identifier_d(x))
        current_q = self.df_m2.at[0, 'Quarter']
        self.df_m2 = self.df_m2.loc[self.df_m2['Quarter'] == current_q]
        self.df_m2["Q_avg_FM2LW"] = self.df_m2['Actual_FM2LW'].sort_values(ascending=True).expanding().mean()
        self.df_m2 = self.df_m2.drop(['Quarter'], axis=1)

        self.df_vom2now = self.df_gdpnow.append(self.df_m2, ignore_index=True, sort=False) #Appends second df to end of 1st df
        d = {'Actual_AGDPNO':'first', 'Actual_AGDPNO_lin':'first', 'Actual_FM2LW':'last', 'Q_avg_FM2LW':'last'}
        self.df_vom2now = self.df_vom2now.groupby('DATE', sort=False, as_index=False).agg(d) #Groups df taking 1st the att from 1st df
        self.df_vom2now = self.df_vom2now.sort_values(['DATE'], ascending=True).reset_index(drop=True)
        self.df_vom2now = self.df_vom2now.fillna(method="ffill").fillna(method="bfill")
        self.df_vom2now['Actual_VOM2'] = self.df_vom2now['Actual_AGDPNO_lin']/self.df_vom2now['Q_avg_FM2LW']
        self.df_vom2now = self.df_vom2now.sort_values(['DATE'], ascending=False).reset_index(drop=True)

        if w_sql == 1:
            self.df_vom2now.to_sql(name="VoM2now_quarter", con=self.out, if_exists='replace')
    
    def vom2_q_table(self):
        self.vom2now_table(0)
        vom2_now_q = self.df_vom2now.iloc[0, :]["DATE"][0:7], self.df_vom2now.iloc[0, :]["Actual_VOM2"]
        self.df_vom2q = self.df_vom2.append(pandas.Series(vom2_now_q, index=['DATE','Actual_FVM2']), ignore_index=True).sort_values(axis=0, by=['DATE'], ascending=False).reset_index(drop=True)
        self.df_vom2q['Quarter'] = self.df_vom2q['DATE'].apply(lambda x: self.q_identifier_m(x))
        
    def gdp_q_table(self):
        self.vom2now_table(0)
        self.df_gdpnowq['Quarter'] = self.df_gdpnowq['DATE'].apply(lambda x: self.q_identifier_m(x))
        
    def gdp_vom2_q_table(self, w_sql=1):
        self.vom2_q_table()
        self.gdp_q_table()
        self.df_vom2q.rename(columns={'DATE':'DATE_FVM2'}, inplace=True)
        self.df_gdpnowq.rename(columns={'DATE':'DATE_FGDPNQ'}, inplace=True)
        #self.df_gdp_vom2_q = pandas.concat([self.df_vom2q, self.df_gdpnowq], axis=1, sort=False, join='outer')
        self.df_gdp_vom2_q = pandas.merge(left=self.df_gdpnowq, right=self.df_vom2q, on='Quarter', left_index=True)
        
        if w_sql == 1:
            self.df_vom2now.to_sql(name="GDP_vs_Vom2_quarterly", con=self.out, if_exists='replace')

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = cvo2m_tables(con, out)
    obj.gdp_vom2_q_table()