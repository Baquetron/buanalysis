import sqlite3
import generic.three_year_comparator as three_year_comparator
import finantials.loans_to_delinq_comparator as loans_to_delinq_comparator
import generic.simple_table as simple_table

class crestatedash:

    def __init__(self, con, out, to_sql=True):
        self.con = con
        self.out = out
        self.to_sql = to_sql

    def execute(self):
        simple_table.simple_table_to_plot(self.con, self.out, 65, "10YB_vs_30Y_fixed_rate_mortgage", "F10YBM", "F30YFRMM")
        three_year_comparator.generate(self.con, self.out, "Mortgage _backed_securities", "FMBSW")
        loans_to_delinq_comparator.generate(self.con, self.out, "RE_loans_vs_delinquency_rate", "FRELACBPCHQ", "GREDRQ")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "House_price_index_vs_inflation", "FPOHPIPC1M", "FCPICH1M")
        three_year_comparator.generate(self.con, self.out, "New_building_permits", "FNPHUM")

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = crestatedash(con, out)
    obj.execute()