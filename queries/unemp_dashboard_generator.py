import sqlite3
import finantials.loans_comparator as loans_comparator
import finantials.loans_to_delinq_comparator as loans_to_delinq_comparator
import generic.simple_table as simple_table
import generic.three_year_comparator as three_year_comparator
import unemployment.unemp_by_sector_table as unemp_by_sector_table
import generic.simple_table as simple_table

class cunempdash:

    def __init__(self, con, out, to_sql=True):
        self.con = con
        self.out = out
        self.to_sql = to_sql

    def execute(self):
        unemp_by_sector_table.generator(con, out, "Unemployment_by_sector", "FURMQOM", "FURCM", "FURDGM", "FURNDGM", "FURMWRM", "FURTUM", "FURIM", "FURFAM", "FURPBSM", "FUREHM", "FURLHM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "Unemployment_by_macrosector", "FURAM", "FURNAM", "FURAIGM", "FURAISEUUFM")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "Initial_jobless_claims", "FICW")
        three_year_comparator.generate(self.con, self.out, "JOLTS_total_non-farm", "FJOTNW")
        three_year_comparator.generate(self.con, self.out, "Total_non-farm_payrolls", "FTNFPM")
        three_year_comparator.generate(self.con, self.out, "ADP_Total_non-farm", "FTNPPM")
        three_year_comparator.generate(self.con, self.out, "Average_hourly_earnings", "FAHEM")

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = cunempdash(con, out)
    obj.execute()