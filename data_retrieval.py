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

def Investing_data_download():
    matrix = {}
    s_date = "Date"
    s_actual = "Actual"
    s_forecast = "Forecast"
    r = re.compile('.*,.*')
    l = re.compile('.*:.*')
    last_date = 0
    # Adavanced web scraping
    click_load_more()
    # Basic web scraping
    page = requests.get(_INVESTING_URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')
    containers = soup.findAll('table', {'class':'genTbl openTbl ecHistoryTbl'})
    for table in containers:
        for td in table.findAll('td'):  #Problem! No way to notice if actual value is shown or not and added blank to matrix
            try:
                text = td.text
                if r.match(text):
                    last_date = 1   #Can be designed to send to 2 if no actual num is founded
                    date_list = text.split(" ")
                    datetime_object = datetime.datetime.strptime(date_list[0], "%b")
                    month_num = datetime_object.month
                    date_str = date_list[1].strip(",") + "/" + str(month_num) + "/" + date_list[2]
                    if s_date in matrix:
                        matrix[s_date].append(date_str)
                    else:
                        matrix[s_date] = [date_str]
                    print(date_str)
                elif l.match(text):
                    pass
                else:
                    if last_date == 1:  #Means last processed text is a date so next text is actual number
                        if s_actual in matrix:
                            matrix[s_actual].append(float(text))
                        else:
                            matrix[s_actual] = [float(text)]
                        print(text)
                        last_date = 2
                    elif last_date == 2:    #Means last processed text is actual num so next text is forecast num
                        if s_forecast in matrix:
                            matrix[s_forecast].append(float(text))
                        else:
                            matrix[s_forecast] = [float(text)]
                        print(text)
                        last_date = 0
            except:
                pass
    #print(matrix)
    df = pandas.DataFrame.from_dict(matrix)[[s_date, s_actual, s_forecast]]
    print df

def click_load_more():
    table_rows = []
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    # Obtain current dir and add string
    try:
        driver = webdriver.Chrome("tools/bin/chromedriver", chrome_options=options)
    except:
         driver = webdriver.Chrome("tools/bin/chromedriver.exe", chrome_options=options)

    driver.get("https://www.investing.com/economic-calendar/investing.com-eur-usd-index-1155")
    # Cookies popup
    WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='TrustArc Cookie Consent Manager']")))
    try:    # Spanish version
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Entendido']"))).click()
        print("Spanish version")
    except: # English version
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Got it']"))).click()
        print("English version")
    # End of cookies

    # PromoteSignUpPopUp
    # Suscription promo erase
    # Take note from this selector search
    #WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#PromoteSignUpPopUp div.right i.popupCloseIcon.largeBannerCloser'))).click()
    """try:
        #myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body div.generalOverlay.js-general-overlay.displayNone.js-promotional')))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'PromoteSignUpPopUp')))
        print ("Elem found")
        #element = driver.find_element_by_css_selector('body > div.generalOverlay.js-general-overlay.displayNone.js-promotional')
        element = driver.find_element_by_id('PromoteSignUpPopUp')
        driver.execute_script("var element = arguments[0];element.parentNode.removeChild(element);", element)
        print ("Pop-up Negated")
    except TimeoutException:
        print("No Pop-Up Detected")"""
    # PromoteSignUpPopUp

    # Put into sight show more button
    show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr>th.left.symbol")))
    driver.execute_script("arguments[0].scrollIntoView(true);",show_more_button)
    myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']"))))
    #show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr>th.left.symbol")))
    #myLength = len(WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']"))))
    #print ("myLength: ", myLength)

    while True:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.showMoreReplies.block>a"))).click()
            WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")) > myLength)
            table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl tr[id^='historicEvent']")
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#showMoreHistory1155>a"))).click()
            #WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']")) > myLength)
            #table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']")
            myLength = len(table_rows)
        except TimeoutException:
            break
    #html = driver.page_source
    #soup = BeautifulSoup(html, 'html.parser')
    #print (soup)
    for row in table_rows:
        print(row.text)
    driver.quit()

if __name__ == "__main__":
    dictionary = parse_json(_JSON_FILE)
    #print(dictionary["Indeces"]["i2"]["name"]) #print specific query values
    #print(json.dumps(dictionary, indent=4)) #print to readable json	
    click_load_more()
