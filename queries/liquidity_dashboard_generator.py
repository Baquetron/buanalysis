import sqlite3
import liquidity.fed_rates_table as fed_rates_table
import liquidity.stock_indeces_table as stock_indeces_table
from liquidity.vom2_tables import cvo2m_tables
import liquidity.bond_yields_table as bond_yields_table
import liquidity.pmi_markit_forecast_table as pmi_markit_forecast_table
import generic.simple_table as simple_table

class cliqdash:

    def __init__(self, con, out, to_sql=True):
        self.con = con
        self.out = out
        self.vo2m_table = cvo2m_tables(con, out)
        self.to_sql = to_sql

    def execute(self):
        # vom2 tables
        self.vo2m_table.vom2now_table() #VoM2now_quarter
        self.vo2m_table.gdp_vom2_q_table()  #GDP_vs_Vom2_quarterly
        # fed rates table
        fed_rates_table.generator(self.con, self.out)
        # stock indices table
        stock_indeces_table.generate(self.out)
        # bond rates tables
        bond_yields_table.generate_bonds_curve(self.con, self.out)
        bond_yields_table.generate_TIPS_table(self.con, self.out)
        # pmi markit forecast table
        pmi_markit_forecast_table.generate(self.con, self.out)
        # simple tables
        simple_table.simple_table_to_plot(self.con, self.out, "M2_supply_biweekly(%)", "FM2W")
        simple_table.simple_table_to_plot(self.con, self.out, "Liquidity_excess_quarterly(%)", "FGDPQ", "FM2Q")
        #simple_table.simple_table_to_plot(self.con, self.out, "LIBOR_vs_Effective_Fed_rates_monthly", "F3MLM", "FEFFRM")
        simple_table.simple_table_to_plot(self.con, self.out, "FED_total_assets", "FFRTAW")
        simple_table.simple_table_to_plot(self.con, self.out, "Excess_Reserves_of_Depository_Institutions", "FERDIM")
        simple_table.simple_table_to_plot(self.con, self.out, "LESS_weekly", "FLESSW")

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = cliqdash(con, out)
    obj.execute()