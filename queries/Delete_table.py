import sqlite3
import pandas

#conn = sqlite3.connect("data/db/economic_data.sqlite")
conn = sqlite3.connect("data/db/dashboard_data.sqlite")

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists
table_name = "GDPNOW_current_quarter"
cursor.execute("DROP TABLE " + table_name)
print("Table dropped... ")

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()