import http.client
import mimetypes
import pandas
import requests
import datetime
import time
import re
import json

_ZILLOW_API_KEY = "X1-ZWz1hz1e1ixma3_9zlkj"

conn = http.client.HTTPSConnection("https://api.bridgedataoutput.com/api/v2/zgecon")
payload = ''
headers = {}
conn.request("GET", "/type?access_token=X1-ZWz1hz1e1ixma3_9zlkj&metadataType=timePeriodType", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))