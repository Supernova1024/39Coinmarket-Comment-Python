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

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
        
    
def watchlist(session,coinurl,amountOftimes):
    if __name__ == "__main__":
        print("Started")
        ua = UserAgent()
        user_agent = ua.chrome
        
        
        # SETUP PROXY WITH AUTHENTICATION
        seleniumwire_options = {
        }
        
        
        options = Options()
        #PROXY = "195.154.255.118:15001"
        #options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument('--window-size=1980,1980')
        #options.add_argument('--headless')
        
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
        
        # Add user login session
        driver.execute_script("window.localStorage.setItem('{}',{})".format("u", json.dumps(session)))
        driver.refresh()
        
        user_email = session
        user_email = find_between( user_email, 'email":"', '","username' )
        print("Logged in to: "+str(user_email))
        

        
        # Click on the Searchbox
    
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]')))
        except Exception:
            print("Exception occured: 2")
            
        inputSearch1 = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div[1]')
        inputSearch1.click()
        
        # Click on the Second Searchbox that extends
        
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="tippy-content"]/div/div/div[1]/div[1]/input')))
        except Exception:
            print("Exception occured: 3")
            
        inputSearch2 = driver.find_element(By.XPATH,'//*[@class="tippy-content"]/div/div/div/div/input')
        inputSearch2.click()
        time.sleep(5)
        # Insert name of the coin to search for
        inputSearch2.send_keys(coinurl)
        inputSearch2.send_keys(Keys.ENTER)


    
        print("Searched for: "+str(coinurl))

        #Wait for page to fully load        
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/h2')))
            print("Coin page Loaded")
        except Exception:
            print("Exception occured: 6")

        time.sleep(3)
        
        #Check if coin already on watchlist
        if len(driver.find_elements(By.XPATH,'//*[@class="icon-Star-Filled"]'))>0:
            print("SKIPPED. Coin already on watchlist")
        elif len(driver.find_elements(By.XPATH,'//*[@class="icon-Star"]'))>0:
            addWatchlist = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/span/button/span')
            addWatchlist.click()
            amountOftimes +=1
            print("Coin added to watchlist. x"+str(amountOftimes))
        else:
            print("UNKNOWN ERROR")
        
        voteID = driver.execute_script("return localStorage.getItem('voteID');")
        print("voteID: "+str(voteID))

        #botaoWatchList = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/span/button/span')
        #botaoWatchList.click()
        print("####################################")
        downVote = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[3]/div/div[1]/div[2]/div[4]/div/div[2]/button[2]')
        downVote.click()

        time.sleep(1110)
        driver.quit()
        
        
amountOftimes = 0

with open("sessions_selenium.txt") as file:
    sessions = file.read().splitlines()

#range is the number of exceptions it handles until it just doesnt try to run the main script again
for session in sessions:
    for i in range(1, 5000):
        try:
            watchlist(session,coinurl,amountOftimes)
        except Exception as e:
            print (e)
            print('#####################################################')
            print('UNKNOWN EXCEPTION OCCURED, Restarting main function!')
            print('#####################################################')
            continue
        else:
            break
            
            
            # RESOLVER O AMOUNTOFTIMES SO DAR X1 E VOLTAR A 0
            # ADICIONAR MULTITHREADING
            
    
    
    
    
