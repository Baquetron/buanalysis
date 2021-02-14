import sqlite3
import generic.simple_table as simple_table
import generic.three_year_comparator as three_year_comparator
import finantials.loans_to_delinq_comparator as loans_to_delinq_comparator

class cunempdash:

    def __init__(self, con, out, to_sql=True):
        self.con = con
        self.out = out
        self.to_sql = to_sql

    def execute(self):
        three_year_comparator.generate(self.con, self.out, "Avg_hourly_earnings", "FAHEM")
        three_year_comparator.generate(self.con, self.out, "Unemployment_rate", "FURM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "Real_disposable_personal_income_vs_personal_saving_rate", "FRDPIM", "FPSRM")
        three_year_comparator.generate(self.con, self.out, "Consumer_sentiment_Michigan", "IMCSM")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "Consumer_curent_vs_expectations_conds", "IMCCM", "IMCEM")
        three_year_comparator.generate(self.con, self.out, "Conumser_loans", "FCLACBPCHM")
        loans_to_delinq_comparator.generate(self.con, self.out, "Cons_loans_vs_delinquency_rate", "FCLACBPCHQ", "GCLDRQ")
        three_year_comparator.generate(self.con, self.out, "Iventories_to_sales_ratio", "FISRM")
        three_year_comparator.generate(self.con, self.out, "CPI", "CPIAUCSL")
        simple_table.simple_table_to_plot(self.con, self.out, 13, "Retail_vs_core_retail_sales", "FRFSTM", "FRFEMVM")
        three_year_comparator.generate(self.con, self.out, "Retail_sales", "FRFSTM")
        three_year_comparator.generate(self.con, self.out, "Total Vehicle Sales", "FTVSM")
        