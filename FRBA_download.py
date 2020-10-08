from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import glob
import pandas

def download():
    filename = "WuXiaShadowRate.xlsx"
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("tools/bin/gc84/chromedriver.exe", chrome_options=options)
    except:
        driver = webdriver.Chrome("tools/bin/chromedriver", chrome_options=options)
    # Minimize browser
    #driver.set_window_position(-2000,0)
    time.sleep(3)
    driver.get("https://www.frbatlanta.org/cqer/research/wu-xia-shadow-federal-funds-rate")

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div/div[2]/div[5]/div/ul[1]/li[2]/a"))).click()
    time.sleep(10)  # Wait for download

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
        shadow_r_reader(filepath)
    else:
        print("%s isn't a file!" % filepath)
        return False
    driver.quit()

def shadow_r_reader(filepath):
    pd_sheet = pandas.read_excel(filepath, sheet_name='Data')
    wuxia_pd = pd_sheet.iloc[:,[0,2]]
    wuxia_pd = wuxia_pd.iloc[::-1]

    wuxia_pd.to_csv("data/AWXSFRM.csv")

def gdpnow_reader(filepath):
    pd_sheet = pandas.read_excel(filepath, sheet_name='TrackingHistory')
    pd_sheet.to_csv("GPDNOW.csv")

if __name__ == "__main__":
    download()
    #shadow_r_reader("/Users/inigo/Downloads/WuXiaShadowRate.xlsx")