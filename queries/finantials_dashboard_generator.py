import sqlite3
import finantials.loans_comparator as loans_comparator
import finantials.loans_to_delinq_comparator as loans_to_delinq_comparator
import generic.simple_table as simple_table

class cliqdash:

    def __init__(self, con, out, to_sql=True):
        self.con = con
        self.out = out
        self.to_sql = to_sql

    def execute(self):       
        simple_table.simple_table_to_plot(self.con, self.out, 26, "FED_total_assets", "FFRTAW")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "Overnight Repurchase Agreements: Treasury Securities Purchased", "FOVRAD")
        simple_table.simple_table_to_plot(self.con, self.out, 13,"Total_Reserves_of_Depository_Institutions_vs_Reserves_Balances_Required", "FTRDIM", "FRBRM")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "LESS_weekly", "FLESSW")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "Loans,_all_commercial_banks", "FCILACBW", "FRELACBW", "FCLACBW")
        simple_table.simple_table_to_plot(self.con, self.out, 26, "Total_assets_vs_liabilities_vs_cash,_all_commercial_banks", "FCAACBW", "FTAACBW", "FTLACBW")
        loans_comparator.generate(self.con, self.out, "CI_loans_by_year", "FCILACBPCHM")
        loans_comparator.generate(self.con, self.out, "RE_loans_by_year", "FRELACBPCHM")
        loans_comparator.generate(self.con, self.out, "CL_loans_by_year", "FCLACBPCHM")
        loans_to_delinq_comparator.generate(self.con, self.out, "CI_loans_vs_delinquency_rate", "FCILACBPCHQ", "GCIDRQ")
        loans_to_delinq_comparator.generate(self.con, self.out, "RE_loans_vs_delinquency_rate", "FRELACBPCHQ", "GREDRQ")
        loans_to_delinq_comparator.generate(self.con, self.out, "Cons_loans_vs_delinquency_rate", "FCLACBPCHQ", "GCLDRQ")

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    obj = cliqdash(con, out)
    obj.execute()