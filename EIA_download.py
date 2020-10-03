import pandas
import requests
import datetime

_API_KEY = "13e2215d2b3ba7e4e849574e2a7f5646"
_DATE_START = "2014-01-01"
_DATE_END = "2021-01-01"

def download(json_dict, name_dict):
    final_data = []
    url = "http://api.eia.gov/series/?api_key=" + _API_KEY + "&series_id=" +  json_dict['Id']
    r = requests.get(url)
    json_data = r.json()
    
    df = pandas.DataFrame(json_data.get("series")[0].get("data"), columns = ["Date", "Actual"])
    df.set_index("Date", drop=True, inplace=True)
    final_data.append(df)
    
    crude = pandas.concat(final_data, axis=1)
    crude["Year"] = crude.index.astype(str).str[:4]
    crude["Month"] = crude.index.astype(str).str[4:]
    crude["Day"] = 1
    crude["Date"] = pandas.to_datetime(crude[["Year", "Month", "Day"]])
    crude.set_index("Date",drop=True,inplace=True)
    crude.sort_index(inplace=True)
    crude = crude[_DATE_START:_DATE_END]
    crude = crude.iloc[:,:5]
    
    crude.to_csv("data/" + name_dict + ".csv")
    return True