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
import PMI_cleaner

#_INVESTING_URL = "https://www.investing.com/economic-calendar/manufacturing-pmi-829"

def download(json_dict, name_dict):
    table_rows = []
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("tools/bin/chromedriver", chrome_options=options)
    except:
        driver = webdriver.Chrome("tools/bin/gc84/chromedriver.exe", chrome_options=options)
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

    while True:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
            WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
            table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")
            myLength = len(table_rows)
        except TimeoutException:
            break

    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
    #WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
    #table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")
    headers = ["Release_M", "Release_D", "Release_Y", "Actual_M", "Release_H", "Actual", "Forecast", "Prev"]
    for i, row in enumerate(table_rows):
        line = str(row.text).replace(",", "").replace("(", "").replace(")", "").split()
        if i == 0:
            prev = line.pop()
            if len(line) == len(headers)-2: #Actual missing
                forecast = line.pop()
                line.extend(['0',forecast,prev]) 
            elif len(line) == len(headers)-3:   #Actual and Forecast missing
                line.extend(['0','0',prev])
            matrix = [line]
        else:
            matrix.append(line)

    table = pandas.DataFrame(matrix, columns=headers)
    # Get to csv
    #path = "data/" + name_dict + "_temp.csv"
    path = "data/" + name_dict + ".csv"
    table.to_csv(path)
    driver.quit()

    if name_dict == "IPMIM":    # Special data preparation for PMI
        PMI_cleaner.execute(path)

    return True

"""if __name__ == "__main__":
    index = {
		"name": "U.S. Manufacturing Purchasing Managers Index (PMI)",
		"src": "Investing",
		"freq": "m",
		"forecast": "Y",
		"src_link": "https://www.investing.com/economic-calendar/manufacturing-pmi-829"
	}
    download(index, "IPMIM")"""