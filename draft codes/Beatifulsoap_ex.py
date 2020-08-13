import pandas
from bs4 import BeautifulSoup
import requests
import datetime
import time
import re

def Investing_data_download():
    matrix = {}
    s_date = "Date"
    s_actual = "Actual"
    s_forecast = "Forecast"
    r = re.compile('.*,.*')
    l = re.compile('.*:.*')
    last_date = 0

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