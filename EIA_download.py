import pandas
import requests
import datetime
import sqlite3

_API_KEY = "13e2215d2b3ba7e4e849574e2a7f5646"
_DATE_START = "2014-01-01"
_DATE_END = "2021-01-01"

def download(json_dict, name_dict):
    freq = json_dict['freq']
    final_data = []
    url = "http://api.eia.gov/series/?api_key=" + _API_KEY + "&series_id=" +  json_dict['Id']
    r = requests.get(url)
    json_data = r.json()
    year = "Y_" + name_dict
    month = "M_" + name_dict
    day = "D_" + name_dict
    actual_date = "Actual_Date_" + name_dict
    actual = "Actual_" + name_dict
    
    df = pandas.DataFrame(json_data.get("series")[0].get("data"), columns = [actual_date, actual])
    df.set_index(actual_date, drop=True, inplace=True)
    final_data.append(df)
    
    crude = pandas.concat(final_data, axis=1)
    if freq == "w":
        crude["Year"] = crude.index.astype(str).str[:4]
        crude["Month"] = crude.index.astype(str).str[4:6]
        crude["Day"] = crude.index.astype(str).str[6:]
    elif freq == "m":
        crude["Year"] = crude.index.astype(str).str[:4]
        crude["Month"] = crude.index.astype(str).str[4:]
        crude["Day"] = 1
        
    crude[actual_date] = pandas.to_datetime(crude[["Year", "Month", "Day"]])
    crude.set_index(actual_date,drop=True,inplace=True)
    crude.sort_index(inplace=True)
    crude = crude[_DATE_START:_DATE_END]
    crude = crude.iloc[:,:5]
    
    table = crude.iloc[: , [0]].copy()
    table = table.reset_index()
    
    reversed_table = table.iloc[::-1]
    reversed_table = reversed_table.reset_index(drop=True)

    #crude.to_csv("data/" + name_dict + ".csv")
    con = sqlite3.connect("data/db/economic_data.sqlite")
    reversed_table.to_sql(name=name_dict, con=con, if_exists='replace')
    return True

if __name__ == "__main__":
    mydict = {
		"name": "Gulf coast refinery and blender net input of crude oil",
		"src": "EIA",
		"freq": "m",
		"Id": "PET.MCRRIP32.M"
	}
    namedict = "EPETM"
    download(mydict, namedict)