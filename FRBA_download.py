from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import glob
import pandas
import sqlite3
from datetime import datetime

def download(json_dict, name_dict):
    filename = json_dict["filename"]
    freq = json_dict["freq"]
    # This is for mac
    home = os.path.expanduser("~")
    filedir = os.path.join(home, "Downloads/")
    # For windows
    """if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ] 

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff
    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)"""

    filepath = filedir + filename
    if os.path.isfile(filepath):
        print("Removing old file")
        os.remove(filepath)

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("tools/bin/gc84/chromedriver.exe", chrome_options=options)
    except:
        driver = webdriver.Chrome("tools/bin/chromedriver", chrome_options=options)
    # Minimize browser
    driver.set_window_position(-2000,0)
    time.sleep(3)
    driver.get(json_dict["src_link"])
    if name_dict == "AWXSFRM":
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div/div[2]/div[5]/div/ul[1]/li[2]/a"))).click()
    elif name_dict == "AGDPNO":
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div[1]/div[1]/p[4]/a[2]"))).click()
    else:
        print("Unknown index!")
        return False
    time.sleep(10)  # Wait for download

    if os.path.isfile(filepath):
        if name_dict == "AWXSFRM":   # Wuxia shadow rates
            shadow_r_reader(filepath, name_dict, freq)
        elif name_dict == "AGDPNO":  # GPDnow
            gdpnow_reader(filepath, name_dict, freq)
    else:
        print("%s isn't a file!" % filepath)
        driver.quit()
        return False
    driver.quit()
    return True

def shadow_r_reader(filepath, name_dict, freq):
    pd_sheet = pandas.read_excel(filepath, sheet_name='Data')
    wuxia_pd = pd_sheet.iloc[:,[0,2]]
    wuxia_pd = wuxia_pd.iloc[::-1].reset_index(drop=True)
    wuxia_pd.columns = ['Actual_Date', 'Actual']

    if freq == "d" or freq == "w" or freq == "o":
        pass
    elif freq == "m" or freq == "q":
        wuxia_pd["Actual_Date"] = wuxia_pd["Actual_Date"].apply(lambda x: str(x)[0:7])
    elif freq == "y":
        wuxia_pd["Actual_Date"] = wuxia_pd["Actual_Date"].apply(lambda x: str(x)[0:4])

    #wuxia_pd.to_csv("data/" + name_dict + ".csv")
    con = sqlite3.connect("data/db/economic_data.sqlite")
    wuxia_pd.to_sql(name=name_dict, con=con)

def gdpnow_reader(filepath, name_dict, freq):
    pd_sheet = pandas.read_excel(filepath, sheet_name='TrackingHistory')
    for i, elem in enumerate(pd_sheet.iloc[:,1]):
        if elem == "GDP Nowcast":
            gdp_pos = i
            break

    gdp_series = pd_sheet.iloc[gdp_pos][2:]
    gdp_pd = gdp_series.reset_index(drop=False)
    gdp_pd.columns = ["Actual_Date", "Actual"]
    gdp_pd = gdp_pd[::-1].reset_index(drop=True)

    if freq == "d" or freq == "w" or freq == "o":
        pass
    elif freq == "m" or freq == "q":
        gdp_pd["Actual_Date"] = gdp_pd["Actual_Date"].apply(lambda x: str(x)[0:7])
    elif freq == "y":
        gdp_pd["Actual_Date"] = gdp_pd["Actual_Date"].apply(lambda x: str(x)[0:4])

    #gdp_pd.to_csv("data/" + name_dict + ".csv")
    con = sqlite3.connect("data/db/economic_data.sqlite")
    gdp_pd.to_sql(name=name_dict, con=con)

if __name__ == "__main__":
    mydict = {
		"name": "Wu-Xia Shadow Federal Funds Rate",
		"src": "FRBAtlanta",
		"freq": "m",
		"filename": "WuXiaShadowRate.xlsx",
		"src_link": "https://www.frbatlanta.org/cqer/research/wu-xia-shadow-federal-funds-rate"
	}
    namedict = "AWXSFRM"
    #download(mydict, namedict)
    shadow_r_reader("/Users/inigo/Downloads/WuXiaShadowRate.xlsx", namedict, "m")
    #gdpnow_reader("/Users/inigo/Downloads/GDPTrackingModelDataAndForecasts.xlsx")
