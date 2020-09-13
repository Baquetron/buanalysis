import sqlite3
import pandas

table = pandas.read_csv(filepath_or_buffer="data/Investing_data.csv", index_col= 0)
table.insert(loc=0, column="Release_Date", value='None')
#table.loc('Release_Y')+table.loc('Release_M')+table.loc('Release_D')
# Join and transform Release_Y-Release_M-Release_D
# Join and transform Actual_M
#con = sqlite3.connect("data/db/economic_data.sqlite")
#table.to_sql(name="Manufacturing_PMI", con=con)
print(table)