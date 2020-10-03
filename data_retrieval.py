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
import FRED_download as FRED
import Investing_download as Investing
import EIA_download as EIA

_JSON_FILE = "indeces.json" #relative path
_API_KEY = 'd03138bb083102e1cfb0f3fe96737854'
_INVESTING_URL = "https://www.investing.com/economic-calendar/manufacturing-pmi-829"

def parse_json(filepath):
    with open(filepath, "r") as f:
        dictionary = json.load(f)
        return dictionary

def acces_json():
    indx_list = parse_json(_JSON_FILE)
    print(indx_list['IPCEM']['source_link'])
    #print(indx_list.keys())

def main():
    ind_dict = parse_json(_JSON_FILE)
    for name in ind_dict:
        if name[0] == "F":  # FRED source
            result = FRED.download(ind_dict[name], name)
            print(result)
        elif name[0] == "I":    # Investing source
            result = Investing.download(ind_dict[name], name)
            print(result)
        elif name[0] == "E":    #EIA source
            result = EIA.download(ind_dict[name], name)
            print(result)

if __name__ == "__main__":
    main()
    #acces_json()
    #FRED_data_donwload()
    #print(dictionary["Indeces"]["i2"]["name"]) #print specific query values
    #print(json.dumps(dictionary, indent=4)) #print to readable json	
    #click_load_more()
