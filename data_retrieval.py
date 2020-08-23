from fred import Fred
import pandas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import datetime
import time
import re
import json

_JSON_FILE = "indeces.json" #relative path
_API_KEY = 'd03138bb083102e1cfb0f3fe96737854'
_INVESTING_URL = "https://www.investing.com/economic-calendar/manufacturing-pmi-829"

def parse_json(filepath):
    with open(filepath, "r") as f:
        dictionary = json.load(f)
        return dictionary
        
def FRED_data_donwload():
    fr = Fred(api_key=_API_KEY,response_type='df')

    params = {
            #'limit':5,
            'output_type': 1,
            "observation_start": "2019-01-01",
            "sort_order": "desc",
            "units": "pch"
            }

    res = fr.series.observations('PCEPILFE', params=params)

    print(res)
    res.to_csv("data/Indeces_data.csv")

def click_load_more():
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
    driver.get(_INVESTING_URL)
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
            temp = line.pop()
            line.extend(['0','0',temp])
            matrix = [line]
        else:
            matrix.append(line)
    # Get to csv
    df = pandas.DataFrame(matrix, columns=headers)
    df.to_csv("data/Investing_data.csv")
    driver.quit()

if __name__ == "__main__":
    dictionary = parse_json(_JSON_FILE)
    #print(dictionary["Indeces"]["i2"]["name"]) #print specific query values
    #print(json.dumps(dictionary, indent=4)) #print to readable json	
    click_load_more()
