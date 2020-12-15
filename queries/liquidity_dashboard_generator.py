import sqlite3
import liquidity.fed_rates_table as fed_rates_table
import liquidity.stock_indeces_table as stock_indeces_table
from liquidity.vom2_tables import cvo2m_tables
import liquidity.bond_rates_table as bond_rates_table
import generic.simple_table as simple_table

class cliqdash:

    def __init__(self, con, out, to_sql=True)
        self.con = con
        self.out = out
        self.vo2m_table = cvo2m_tables(con, out)
        self.to_sql = to_sql

    def execute(self):
        # vom2 tables

        # fed rates table

        # stock indices table

        # bond rates tables

        # simple tables
        pass

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = cliqdash(con, out, False)