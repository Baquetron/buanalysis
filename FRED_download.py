from fred import Fred
import pandas
import sqlite3
from datetime import datetime

_API_KEY = 'd03138bb083102e1cfb0f3fe96737854'
_DATE_START = "2014-01-01"

def download(json_dict, name_dict):
    fr = Fred(api_key=_API_KEY,response_type='df')
    freq = json_dict['freq'],
    params = {
            "output_type": 1,
            "observation_start": _DATE_START,
            "frequency": freq,
            "sort_order": "desc",
            "units": json_dict['units']
            }

    res = fr.series.observations(json_dict['Id'], params=params)
    res = res.drop(['realtime_end', 'realtime_start'], axis=1)
    res.columns = ["Actual_Date", "Actual"]

    if freq == "d" or freq == "w" or freq == "o":
        pass
    elif freq == "m" or freq == "q":
        res["Actual_Date"] = res["Actual_Date"].apply(lambda x: str(x)[0:7])
    elif freq == "y":
        res["Actual_Date"] = res["Actual_Date"].apply(lambda x: str(x)[0:4])

    #res.to_csv("data/" + name_dict + ".csv")
    con = sqlite3.connect("data/db/economic_data.sqlite")
    res.to_sql(name=name_dict, con=con)

    return True

if __name__ == "__main__":
        """mydict = {
		"name": "3-Month London Interbank Offered Rate (LIBOR)",
		"src": "FRED",
		"freq": "d",
		"units": "lin",
		"Id": "USD3MTD156N"
	}
        name = "F3MLD"""

        mydict = {
		"name": "M2 Money Stock",
		"src": "FRED",
		"freq": "w",
		"units":"chg",
		"Id": "M2"
	}
        name = "FM2W"
        download(mydict, name)