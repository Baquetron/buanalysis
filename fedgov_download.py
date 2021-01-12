from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas
import requests
import datetime
import time
import sqlite3

def download(json_dict, name_dict, to_sql=True):
    headers = ["Actual_Date_", "RE_all_", "RE_residential_", "RE_commercial_", "RE_farmland_", "CL_all_", "CL_credit_cards_", "CL_others_", "Leases_", "CI_all_", "Agricultural_", "Total_loans_and_leases_"]
    FGREDRQ_headers = headers[0:5]
    FGCIDRQ_headers = ["Actual_Date_", "CI_all_"]
    FGCLDRQ_headers = ["Actual_Date_", "CL_all_", "CL_credit_cards_", "CL_others_"]

    table_rows = []
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("tools/bin/gc84/chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("tools/bin/chromedriver", options=options)
    # Minimize browser
    #driver.set_window_position(-2000,0)
    time.sleep(3)
    driver.get(json_dict['src_link'])

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='date1']")))

    table_rows = driver.find_elements_by_css_selector("table.statistics tr")

    init_row = 0
    for i, row in enumerate(table_rows):
        line = str(row.text).replace('n.a.', 'NaN').replace(':', '-').split()
        if i == init_row:
            matrix = [line]
        else:
            matrix.append(line)

    matrix = matrix[3:]
    table = pandas.DataFrame(matrix, columns=headers)

    driver.quit()

    if name_dict == "GREDRQ":
        table = table[FGREDRQ_headers]
    elif name_dict == "GCIDRQ":
        table = table[FGCIDRQ_headers]
    elif name_dict == "GCLDRQ":
        table = table[FGCLDRQ_headers]

    table.rename(columns={table.columns.values[1]: "Actual_"}, inplace=True)
    table.columns = [s + name_dict for s in table.columns.values]
    
    if to_sql == True:
        con = sqlite3.connect("data/db/economic_data.sqlite")
        table.to_sql(name=name_dict, con=con, if_exists='replace')
    else:
        print(table)
        table.to_csv("data/" + name_dict + ".csv")

if __name__ == "__main__":
    index = {
        "name": "U.S. RE Delinquency rates",	
        "src": "Fedgov",	
        "freq": "q",
        "src_link": "https://www.federalreserve.gov/releases/chargeoff/delallsa.htm"
    }
    download(index, "GREDRQ", True)