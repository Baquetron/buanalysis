import sqlite3
import liquidity.fed_rates_table as fed_rates_table
import liquidity.bond_yields_table as bond_yields_table
import generic.simple_table as simple_table

class cinfldash:

    def __init__(self, con, out, to_sql=True):
        self.con = con
        self.out = out
        self.to_sql = to_sql

    def execute(self):
        fed_rates_table.generator(self.con, self.out)
        bond_yields_table.generate_TIPS_table(self.con, self.out)
        simple_table.simple_table_to_plot(self.con, self.out, 648, "10y_breakeven_yoy_vs_10y_yield", "F10YBICH1W", "F10YBW")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "10-Y_Breakeven_Inflation", "F10YBIW", "F10YBICHW")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "5-Y_5-Y_Forward_Inflation", "F5YFIEW", "F5YFIECHW")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "2y_vs_10y_Treasury", "F2YBW", "F10YBW")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "CPI", "FCPIM", "FCPICHM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "PCE", "FPCEM", "FPCECHM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "PPI", "FPPIM", "FPPICHM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "Michigan_5y_inflation_expectation", "IM5YIM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "ISM_Manu_vs_Non-Manu_prices", "IMPISMM", "INMPISMM")

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = cinfldash(con, out)
    obj.execute()