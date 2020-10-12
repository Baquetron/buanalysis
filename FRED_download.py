from fred import Fred
import pandas

_API_KEY = 'd03138bb083102e1cfb0f3fe96737854'
_DATE_START = "2014-01-01"

def download(json_dict, name_dict):
    fr = Fred(api_key=_API_KEY,response_type='df')
    params = {
            "output_type": 1,
            "observation_start": _DATE_START,
            "frequency": json_dict['freq'],
            "sort_order": "desc",
            "units": json_dict['units']
            }

    res = fr.series.observations(json_dict['Id'], params=params)
    res = res.drop(['realtime_end', 'realtime_start'], axis=1)
    res.to_csv("data/" + name_dict + ".csv")

    return True

if __name__ == "__main__":
        mydict = {
		"name": "3-Month London Interbank Offered Rate (LIBOR)",
		"src": "FRED",
		"freq": "d",
		"units": "lin",
		"Id": "USD3MTD156N"
	}
        name = "F3MLD"
        download(mydict, name)