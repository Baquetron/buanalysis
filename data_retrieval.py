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
         driver = webdriver.Chrome("tools/bin/chromedriver.exe", chrome_options=options)

    # Minimize browser
    driver.set_window_position(-2000,0)
    driver.get(_INVESTING_URL)
    # Cookies popup
    WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='TrustArc Cookie Consent Manager']")))
    try:    # Spanish version
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Entendido']"))).click()
    except: # English version
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Got it']"))).click()
    # End of cookies

    # Put into sight show more button
    show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr>th.left.symbol")))
    driver.execute_script("arguments[0].scrollIntoView(true);",show_more_button)
    myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']"))))
    #show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr>th.left.symbol")))
    #myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']"))))
    #print ("myLength: ", myLength)

    """while True:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
            WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
            table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#showMoreHistory1155>a"))).click()
            #WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']")) > myLength)
            #table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']")
            myLength = len(table_rows)
        except TimeoutException:
            break"""

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
    WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
    table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")
    print ("Good job!")
    matrix = []
    for row in table_rows:
        print(row.text)
        line = row.text
        matrix.append(line)
    # Get to csv
    df = pandas.DataFrame.from_dict(table_rows)
    df.to_csv("data/Investing_data.csv")
    driver.quit()

if __name__ == "__main__":
    dictionary = parse_json(_JSON_FILE)
    #print(dictionary["Indeces"]["i2"]["name"]) #print specific query values
    #print(json.dumps(dictionary, indent=4)) #print to readable json	
    click_load_more()
