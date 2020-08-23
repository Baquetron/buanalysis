from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import datetime
import time

#Cookies old iframe
WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='TrustArc Cookie Consent Manager']")))

# PromoteSignUpPopUp
# Suscription promo erase
# Take note from this selector search
WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#PromoteSignUpPopUp div.right i.popupCloseIcon.largeBannerCloser'))).click()
try:
    #myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body div.generalOverlay.js-general-overlay.displayNone.js-promotional')))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'PromoteSignUpPopUp')))
    print ("Elem found")
    #element = driver.find_element_by_css_selector('body > div.generalOverlay.js-general-overlay.displayNone.js-promotional')
    element = driver.find_element_by_id('PromoteSignUpPopUp')
    driver.execute_script("var element = arguments[0];element.parentNode.removeChild(element);", element)
    print ("Pop-up Negated")
except TimeoutException:
    print("No Pop-Up Detected")

while True:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#showMoreHistory1155>a"))).click()
            WebDriverWait(driver, 20).until(lambda driver: len(driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']")) > myLength)
            table_rows = driver.find_elements_by_css_selector("table.genTbl.openTbl.ecHistoryTbl#eventHistoryTable1155 tr[event_attr_id='1155']")
            myLength = len(table_rows)
        except TimeoutException:
            break
# PromoteSignUpPopUp