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
from random import randrange
import mysql.connector

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
parser.add_argument('--displayName', type=str, required=True)
parser.add_argument('--username', type=str, required=True)
parser.add_argument('--avatar', type=str, required=True)
parser.add_argument('--quantity', type=str, required=True)

# Parse the argument
args = parser.parse_args()
displayName = args.displayName # DisplayName to change to
username = args.username    # Username to change to ( can only be done every 7 days )
avatar = args.avatar    # Avatar position example: 5 | it will change to the avatar on position 5
quantity = args.quantity    # Avatar position example: 5 | it will change to the avatar on position 5


if len(username)>13:
    print("Username too long, pick another")
    quit()

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
        
    
def updateProfile(session,displayName,username,avatar,amountOftimes):
    if __name__ == "__main__":
        print("Started")
        #print(session)
        ua = UserAgent()
        user_agent = ua.chrome

        
        # SETUP PROXY WITH AUTHENTICATION
        seleniumwire_options = {
        }
        
        
        options = Options()
        options.add_argument('--window-size=1980,1980')
        options.add_argument('--headless')
        
        # FOR PROXY WITH AUTHENTICATION
        driver = Chrome(seleniumwire_options=seleniumwire_options,  options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        actions = ActionChains(driver)

        #Enter Coin Page
        
        try:
            driver.set_page_load_timeout(60)
            url='https://coinmarketcap.com/'
            driver.get(url)
        except Exception:
            print("Exception occured: 1")
            print('Page Loading forever, pressing ESC to stop loading')
            actions.send_keys(Keys.ESC)
            actions.perform()
            
        print("Entered coinmarketcap")
        
        # Add user login session
        driver.execute_script("window.localStorage.setItem('{}',{})".format("u", json.dumps(session)))
        driver.refresh()
        
        user_email = session
        user_email = find_between( user_email, 'email":"', '","username' )
        print("Logged in to: "+str(user_email))
        


        #Enter Profile Page
        try:
            driver.set_page_load_timeout(60)
            url='https://coinmarketcap.com/settings'
            driver.get(url)
        except Exception:
            print("Exception occured: 2")
            print('Page Loading forever, pressing ESC to stop loading')
            actions.send_keys(Keys.ESC)
            actions.perform()
            
        #Change Display Name
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/input')))
        except Exception:
            print("Exception occured: 2")
            
        displayNameInput = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/input')
        displayNameInput.click()
        displayNameInput.send_keys(Keys.CONTROL,"a")
        displayNameInput.send_keys(Keys.DELETE)
        displayNameInput.send_keys(displayName)

        #Change Avatar
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/button')))
        except Exception:
            print("Exception occured: 3")
            
        editAvatarButton = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/button')
        editAvatarButton.click()
        time.sleep(2) # CODE SOMETHING TO WAIT FOR SUBMIT BUTTON TO GO BACK TO BLUE AFTER 3 SECONDS WHICH CONFIRMS FORM WAS SUBMITED
        
        AvatarImage = driver.find_element(By.XPATH,'//*[@id="avatars-lists"]/div['+str(avatar)+']')
        AvatarImage.click()
        
        #Click on Select Avatar Button
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div/button')))
        except Exception:
            print("Exception occured: 4")
        
        selectAvatar = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/button')
        selectAvatar.click()
        time.sleep(2)
        

        #Change Username
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/div[3]/input')))
        except Exception:
            print("Exception occured: 5")
            
        usernameInput = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/div[3]/input')
        usernameInput.click()
        usernameInput.send_keys(Keys.CONTROL,"a")
        usernameInput.send_keys(Keys.DELETE)
        username = username+"_"+str(randrange(999999))
        usernameInput.send_keys(username)

        #Click on SAVE Button
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/button')))
        except Exception:
            print("Exception occured: 6")
        
        saveButton = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[2]/div/div/div/div[2]/button')
        saveButton.click()
        time.sleep(4)

        
        
        #Enter Bitcoin page so the LocalStorage session token data updates
        try:
            driver.set_page_load_timeout(60)
            url='https://coinmarketcap.com/currencies/bitcoin'
            driver.get(url)                
        except Exception:
            print("Exception occured: 6")
            print('Page Loading forever, pressing ESC to stop loading')
            actions.send_keys(Keys.ESC)
            actions.perform()
            
        time.sleep(4)
        
        # Fetch LocalStorage Session
        sessionLocalStorage = driver.execute_script("return localStorage.getItem('u');")
        sessionLocalStorage = sessionLocalStorage

        if session == sessionLocalStorage:
            print("ERROR, PROFILE DIDNT UPDATE! SKIPPING")
        else:
        
            # Update old LocalStorage Session to the new one
            mydb = mysql.connector.connect( host="sql327.main-hosting.eu", user="u830852358_cmc", password="Davide74", database="u830852358_cmc", autocommit=True)
            mycursor = mydb.cursor()
            dateNow = str(datetime.now())
            
            sql = 'UPDATE sessions SET session_selenium = %s, updated = %s, updated_at = %s, updated_displayName = %s, updated_username = %s, updated_avatar = %s  WHERE email = %s'
            values = [sessionLocalStorage,int(1),str(dateNow),str(displayName),str(username),str(avatar),str(user_email)]
            mycursor.execute(sql, values)
            
            if mycursor.rowcount == 1:
                print("PROFILE UPDATED!")
            else:
                print("Debug: "+str(mycursor.rowcount))
                print("Debug: "+str(user_email))
                print("Debug: "+str(mycursor.execute))
    
            
        print("################################")

        time.sleep(5)
        driver.quit()
        
        
        
        
        
        
        
amountOftimes = 0

# Select sessions from Database
mydb = mysql.connector.connect( host="sql327.main-hosting.eu", user="u830852358_cmc", password="Davide74", database="u830852358_cmc", autocommit=True)
mycursor = mydb.cursor()

# Only select sessions that werent updated before, change this to select sessions updated more than 7 days ago as well later
sql = 'SELECT session_selenium FROM sessions WHERE updated = 0 LIMIT '+str(quantity)
mycursor.execute(sql)
sessions = mycursor.fetchall()

# Select sessions from TXT file            
#with open("sessions_selenium.txt") as file:
#    sessions = file.read().splitlines()

#range is the number of exceptions it handles until it just doesnt try to run the main script again


for session in sessions:
    for i in range(1, 5000):
        try:
            updateProfile(session[0],displayName,username,avatar,amountOftimes)
        except Exception as e:
            print (e)
            print('#####################################################')
            print('UNKNOWN EXCEPTION OCCURED, Restarting main function!')
            print('#####################################################')
            continue
        else:
            break
            




    
    
    
