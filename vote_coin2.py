import time
import cv2
import random
import numpy as np
import pyautogui
import bezier
import requests
import os
import re
import sys
import json
import names
import pickle
from datetime import datetime
from requests import get
from fake_useragent import UserAgent
from requests.structures import CaseInsensitiveDict

from seleniumwire.undetected_chromedriver.v2 import Chrome

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.support.ui import WebDriverWait

import argparse



# Disable pyautogui pauses
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

           

        

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('--coinurl', type=str, required=True)

# Parse the argument
args = parser.parse_args()
coinurl = args.coinurl

                


with open("sessions_selenium.txt") as file:
    sessions = file.read().splitlines()

    
def watchlist(session,coinurl):
    if __name__ == "__main__":
    
        ua = UserAgent()
        user_agent = ua.chrome
        
        
        # SETUP PROXY WITH AUTHENTICATION
        seleniumwire_options = {
            'proxy': {
                'http': 'http://oxy123asdx:GbaTTyshca@4g.iproyal.com:4001',
                'https': 'https://oxy123asdx:GbaTTyshca@4g.iproyal.com:4001',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        
        
        options = Options()
        #PROXY = "195.154.255.118:15001"
        #options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument('--window-size=1980,1980')
        options.add_argument('--headless')
        
        # FOR PROXY WITH AUTHENTICATION
        driver = Chrome(seleniumwire_options=seleniumwire_options,  options=options)
        
        #driver = Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


        
        #Enter Coin Page
    
        try:
            driver.set_page_load_timeout(60)
            url='https://coinmarketcap.com/'
            driver.get(url)
        except Exception:
            print("Exception occured: 1")
            print('Page Loading forever, pressing ESC to stop loading')
            pyautogui.press('esc')
            
        print("Entered coinmarketcap")
        driver.execute_script("window.localStorage.setItem('{}',{})".format("u", json.dumps(session)))
        driver.refresh()
        print("Logged in")

        inputSearch1 = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]')
        inputSearch1.click()
        time.sleep(5)
        
        inputSearch = driver.find_element(By.XPATH,'//*[@class="tippy-content"]/div/div/div[1]/div[1]/input')
        inputSearch.click()
        inputSearch.send_keys(coinurl)
        inputSearch.send_keys(Keys.ENTER)
        print("Searched for Coin")

        startWatchlist = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/span/button/span')
        startWatchlist.click()
        print("Added coin to Watchlist")

        
   
        #botaoWatchList = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/span/button/span')
        #botaoWatchList.click()
        time.sleep(5000)


amountOftimes = 0
for session in sessions:
    amountOftimes +=1
    watchlist(session,coinurl)