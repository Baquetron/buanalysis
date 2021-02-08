from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas
import requests
import datetime
import time
import re
import calendar
from time import strptime
import investing_cleaner

def download(json_dict, name_dict, to_sql=True):
    headers = ["Release_M_", "Release_D_", "Release_Y_", "Actual_M_", "Release_H_", "Actual_", "Forecast_", "Prev_"]
    headers = [s + name_dict for s in headers]

    table_rows = []
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("tools/bin/gc84/chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("tools/bin/chromedriver", options=options)
    # Minimize browser
    driver.set_window_position(-2000,0)
    time.sleep(3)
    driver.get(json_dict['src_link'])
    # Cookies popup
    try:
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='onetrust-accept-btn-handler']"))).click()
    except TimeoutException:
        print("Button not found. Check if web has changed!")
    # End of cookies

    # Put into sight show more button
    show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr>th.left.symbol")))
    driver.execute_script("arguments[0].scrollIntoView(true);",show_more_button)
    myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']"))))

    #Erase video elem from lower left video corner
    try:
        element = driver.find_element_by_id('video')
        driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
    except:
        pass

    while True:
        try:
            # Put into sight show more button
            show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr>th.left.symbol")))
            driver.execute_script("arguments[0].scrollIntoView(true);",show_more_button)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
            WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
            table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")
            myLength = len(table_rows)
        except TimeoutException:
            break

    """WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
    WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
    table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")"""

    init_row = 0
    for i, row in enumerate(table_rows):
        line = str(row.text).replace(",", "").replace("(", "").replace(")", "").split()
        if i == init_row:
            prev = line.pop()
            if name_dict == "IPMICMM":
                if len(line) == len(headers)-3:   #Actual and Forecast missing
                    line.extend(['0.0','0.0',prev])
                else:
                    line.extend([prev])
            else:
                if len(line) == len(headers)-1:  #Line ok
                    line.extend([prev])
                elif len(line) == len(headers)-2: #Actual missing
                    forecast = line.pop()
                    line.extend(['0.0',forecast,prev]) 
                elif len(line) == len(headers)-3:   #Actual and Forecast missing
                    line.extend(['0.0','0.0',prev])
                else:   #Bad structured row by Investing: Delete it
                    init_row = 1
                    pass
            matrix = [line]
        else:
            matrix.append(line)

    table = pandas.DataFrame(matrix, columns=headers)
    # Get to csv
    path = "data/" + name_dict + ".csv"
    table.to_csv(path)
    driver.quit()

    if "PMI" in json_dict['name']:  # Special data preparation for PMI
        if "ism" in json_dict['src_link']:
            investing_cleaner.ism_execute(name_dict, to_sql)
        else:
            investing_cleaner.markit_execute(name_dict, to_sql)
    elif "ism" in json_dict['src_link']:
        investing_cleaner.ism_execute(name_dict, to_sql)
    elif "Michigan" in json_dict['name']:
        investing_cleaner.michigan_inflation_execute(name_dict, to_sql)
    return True

if __name__ == "__main__":
    index = {
		"name": "U.S. ISM Non-Manufacturing Prices",	
		"src": "Investing",	
		"freq": "m",	
		"forecast": "Y",	
		"src_link": "https://www.investing.com/economic-calendar/ism-non-manufacturing-prices-1049"	
	}
    download(index, "INMPISMM")