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
import mysql.connector


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

import Xlib.display
pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])

# Disable pyautogui pauses
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

def delete_cache():
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3) # send right combination
    actions.perform()
    time.sleep(2)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER) # confirm
    actions.perform()
    time.sleep(5) # wait some time to finish
    driver.close() # close this tab
    driver.switch_to.window(driver.window_handles[0]) # switch back

# Get captcha solution
def lower_right_piece1():
    bg_img = cv2.imread('captcha/captcha.png')
    tp_img = cv2.imread('captcha/piece1.png')

    bg_pic = bg_img
    tp_pic = tp_img

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # Looking for the best match

    X = max_loc[0]

    th, tw = tp_pic.shape[:2]
    tl = max_loc # The coordinates of the upper left corner
    br = (tl[0]+tw,tl[1]+th) # The coordinates of the lower right corner
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # Draw a rectangle
    cv2.imwrite('piece1_result.jpg', bg_img) # Keep it locally
    return(br)

def lower_right_piece2():
    bg_img = cv2.imread('captcha/captcha.png')
    tp_img = cv2.imread('captcha/piece2.png')

    bg_pic = bg_img
    tp_pic = tp_img

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # Looking for the best match

    X = max_loc[0]

    th, tw = tp_pic.shape[:2]
    tl = max_loc # The coordinates of the upper left corner
    br = (tl[0]+tw,tl[1]+th) # The coordinates of the lower right corner
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # Draw a rectangle
    cv2.imwrite('piece2_result.jpg', bg_img) # Keep it locally
    return(br)
    
def slow_type(pageElem, pageInput):
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        pageElem.send_keys(letter)

def bezier_mouse(location, size, panelHeight): ##move mouse to middle of element
    x, relY = location["x"], location["y"] ##abs X and relative Y
    absY = relY + panelHeight
    w, h = size["width"], size["height"]
    wCenter = w/2
    hCenter = h/2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = xCenter, yCenter

    x2 = (start[0] + end[0]) / 2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2) / 2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to create perfect curve
    control2 = control2X, y2

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.003  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay


def bezier_mouse_x_y(locationX, locationY, size, panelHeight): ##move mouse to middle of element
    x, relY = locationX, locationY ##abs X and relative Y
    absY = relY + panelHeight
    w, h = size["width"], size["height"]
    wCenter = w/2
    hCenter = h/2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = xCenter, yCenter

    x2 = (start[0] + end[0]) / 2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2) / 2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to create perfect curve
    control2 = control2X, y2

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.003  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay

def resting_mouse(): #move mouse to right of screen

    start = pyautogui.position()
    end = random.randint(1600,1750), random.randint(400,850)

    x2 = (start[0] + end[0])/2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2)/2
    control2X = (end[0] + x2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to create perfect curve
    control2 = control2X, y2 ## using y2 for both to get a more linear curve

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.003  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay
    time.sleep(2)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
        
        
#with open("http_proxies.txt") as file_in:
#    proxies = []
#    for line in file_in:
#        proxies.append(line)




#Start Creating CMC Accounts
def main(currentRunNumber,quantityOfAccounts):    
    
    if __name__ == "__main__":
        
        while currentRunNumber in range(quantityOfAccounts):
            currentRunNumber+=1
            print("---------------------------------------------")
            print("Run number: "+str(currentRunNumber)+"/"+str(quantityOfAccounts))
            print("---------------------------------------------")
            restart_script = 0
            
    
            
    
            
            ua = UserAgent()
            user_agent = ua.chrome
            
            #options.add_argument("user-agent="+user_agent)
            #print("User Agent: "+user_agent)


            # SETUP PROXY WITH AUTHENTICATION
            seleniumwire_options = {
                'proxy': {
                    'http': 'http://oxyTragas:YYTtagxasdS@4g.iproyal.com:6061',
                    'https': 'https://oxyTragas:YYTtagxasdS@4g.iproyal.com:6061',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            
            
            # SETUP PROXY WITHOUT AUTHENTICATION
            #seleniumwire_options = {
            #    'proxy': {
            #        'http': 'http://l3atf69o:hA8jRsjokxDzzQoi_country-UnitedStates@proxy.proxy-cheap.com:31112',
            #        'https': 'https://l3atf69o:hA8jRsjokxDzzQoi_country-UnitedStates@proxy.proxy-cheap.com:31112',
            #        'no_proxy': 'localhost,127.0.0.1'
            #    }
            #}
    
    
            options = Options()
            #PROXY = "195.154.255.118:15001"
            #options.add_argument('--proxy-server=%s' % PROXY)
            options.add_argument('--window-size=1980,1980')
            #options.add_argument('--headless')
            
            # FOR PROXY WITH AUTHENTICATION
            driver = Chrome(seleniumwire_options=seleniumwire_options,  options=options)
            
            #driver = Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
            #Create a Random Email hash
            
            
            first_name = names.get_first_name()
            last_name = names.get_last_name()
    
            
            half_length_last = round(len(str(last_name))/2)
            half_length_first = round(len(str(first_name))/2)
            
            half_last_name = last_name[:half_length_last]
            half_first_name = first_name[:half_length_first]
            
            hash_array = []
            
            hasha1 = first_name + last_name + str(random.randint(0,999))
            hasha2 = first_name + str(random.randint(0,999)) + last_name
            hasha3 = str(random.randint(0,999)) + first_name + last_name        
            
            hasha4 = first_name + half_last_name + str(random.randint(0,999))
            hasha5 = first_name + str(random.randint(0,999)) + half_last_name
            hasha6 = str(random.randint(0,999)) + first_name + half_last_name 
            
            hasha7 = half_first_name + last_name + str(random.randint(0,999))
            hasha8 = half_first_name + str(random.randint(0,999)) + last_name
            hasha9 = str(random.randint(0,999)) + half_first_name + last_name
            
            hasha10 = half_first_name + half_last_name + str(random.randint(0,999))
            hasha11 = half_first_name + str(random.randint(0,999)) + half_last_name
            hasha12 = str(random.randint(0,999)) + half_first_name + half_last_name
            
            hasha13 = first_name + last_name + str(random.randint(0,99))
            hasha14 = last_name + first_name + str(random.randint(0,99))
            hasha15 = half_first_name + half_last_name + str(random.randint(0,99))
            hasha16 = half_last_name + half_first_name + str(random.randint(0,99))

            
            hash_array.append(hasha1)
            hash_array.append(hasha2)
            hash_array.append(hasha3)
            hash_array.append(hasha4)
            hash_array.append(hasha5)
            hash_array.append(hasha6)
            hash_array.append(hasha7)
            hash_array.append(hasha8)
            hash_array.append(hasha9)
            hash_array.append(hasha10)
            hash_array.append(hasha11)
            hash_array.append(hasha13)
            hash_array.append(hasha14)
            hash_array.append(hasha15)
            hash_array.append(hasha16)

            
            
            
            hasha = random.choice(hash_array).lower()
    
            print("Email: "+str(hasha)+"@nomadside.com")
        
            erase_cache_cookies = 0
            
            if erase_cache_cookies == 1:
                print("Clearing Cookies and Cache...")
                driver.delete_all_cookies()
                delete_cache()
            
            
            #Get Proxy IP
            
            try:
                driver.set_page_load_timeout(30)
                driver.get('http://api.ipify.org/')
            except Exception:
                print("Exception occured: 0")
                print('Page Loading forever, pressing ESC to stop loading')
                pyautogui.press('esc')
                
    
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.TAG_NAME, "body")))
            except Exception:
                print("Exception occured: 9")
                driver.quit()
                continue
                
            ip = driver.find_element(By.TAG_NAME, "body").text
    
            print('Proxy: {}'.format(ip))
            print("---------------------------------------------")    
        
            #Enter Coinmarketcap
            
            try:
                driver.set_page_load_timeout(60)
                url='https://coinmarketcap.com/methodology/'
                driver.get(url)                
            except Exception:
                print("Exception occured: 1")
                print('Page Loading forever, pressing ESC to stop loading')
                pyautogui.press('esc')
    
            url='http://ip-api.com/json'

            panelHeight = driver.execute_script("return window.outerHeight - window.innerHeight")
        
            print("Signing up...")
    
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[1]/div[2]/button[2]')))
            except Exception:
                print("Exception occured: 2")
                driver.quit()
                continue
                
            botaocriarconta1 = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[1]/div[1]/div[2]/button[2]')
            #bezier_mouse(botaocriarconta1.location, botaocriarconta1.size , panelHeight)
            botaocriarconta1.click()
        
            #resting_mouse()
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/div[3]/input")))
            except Exception:
                print("Exception occured: 3")
                driver.quit()
                continue
    
            inputemail = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[3]/input')
            #bezier_mouse(inputemail.location, inputemail.size , panelHeight)
            #time.sleep(float(random.uniform(.05, .3)))
            inputemail.click()
            
            email = str(hasha)+"@nomadside.com"
            
            inputemail.send_keys(email)
            #slow_type(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[3]/input'),email)
            #resting_mouse()
            
            #time.sleep(float(random.uniform(.05, .3)))
            inputpassword = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[4]/div[2]/input')
            #bezier_mouse(inputpassword.location, inputpassword.size , panelHeight)
            #time.sleep(float(random.uniform(.05, .3)))
            inputpassword.click()
            #resting_mouse()
            
            password = "Cmcforever3218"
    
            #slow_type(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[4]/div[2]/input'),password)
            inputpassword.send_keys(password)

            
            captcha_attempts = 0
            captcha_solved = 0
            
            network_error = 0
            
            while captcha_solved == 0:
            
                if network_error == 1:
                    print("Rotating Proxy!")
                    url = "https://dashboard.iproyal.com/4g-mobile-proxies/rotate-ip/lithuanian/begVEeOcP"
    
                    payload={}
                    headers = {
                    'Content-Type': 'application/json'
                    }
                    
                    response = requests.request("GET", url, headers=headers, data=payload)
                    restart_script = 1
                    print(response.text)
                    print("Restarting for proxy to rotate!")
                    #print("Waiting 1 minute before running script again to let proxy rotate automaticaly!")
                    #time.sleep(60)
                    break

                    
                if captcha_attempts == 0:
                    print("Solving Captcha...")
                
                captcha_attempts+=1
                
                botaocriarconta = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[6]/button')
                #bezier_mouse(botaocriarconta.location, botaocriarconta.size , panelHeight)
                #time.sleep(float(random.uniform(.05, .3)))
                #pyautogui.click()
                botaocriarconta.click()
                #resting_mouse()
                #time.sleep(float(random.uniform(.05, .3)))
                
                if captcha_attempts > 1:
                    print("Solving Captcha... x"+str(captcha_attempts))
                    
                    if captcha_attempts == 4:
                        print("Too many failled captcha retries, reestarting bot!")    
                        print("Rotating Proxy!")
                        url = "https://dashboard.iproyal.com/4g-mobile-proxies/rotate-ip/lithuanian/begVEeOcP"
    
                        payload={}
                        headers = {
                        'Content-Type': 'application/json'
                        }
                        
                        response = requests.request("GET", url, headers=headers, data=payload)
                        restart_script = 1
                        print(response.text)
                        print("Restarting for proxy to rotate!")
                        #print("Waiting 1 minute before running script again to let proxy rotate automaticaly!")
                        #time.sleep(60)
                        break
    
                    
                
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div[1]")))
                except Exception:
                    print("Exception occured: 4")
                    break
                
                time.sleep(3)
                # Screenshot Captcha and save it as captcha.png for OCR
                with open('captcha/captcha.png', 'wb') as file:
                    file.write(driver.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div[1]').screenshot_as_png)
                time.sleep(5)
                
                piece1 = lower_right_piece1()
                piece2 = lower_right_piece2()
                
                difference = piece2[0]-piece1[0]
                
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "html/body/div[4]/div/div[2]/div[1]/div")))
                except Exception:
                    print("Exception occured: 10")
                    break
                    
                source1 = driver.find_element(By.XPATH,'html/body/div[4]/div/div[2]/div[1]/div')
                bezier_mouse(source1.location, source1.size , panelHeight)
                time.sleep(float(random.uniform(.05, .3)))
                pyautogui.mouseDown()
                
                # Random Movements before dropping the puzzle piece to mimic human behaviour
                
                locationX = source1.location["x"] + difference
                locationY = source1.location["y"] + random.randint(1,15)        
                
                locationX_2 = source1.location["x"] + difference + random.randint(15,150)
                locationY_2 = source1.location["y"] + random.randint(-150,-45)
                        
                locationX_3 = source1.location["x"] + difference - random.randint(15,150)
                locationY_3 = source1.location["y"] + random.randint(30,100)
                                
                locationX_4 = source1.location["x"] + difference + random.randint(15,150)
                locationY_4 = source1.location["y"] + random.randint(-50,-15)
                
                locationX_5 = source1.location["x"] + difference + random.randint(-50,50)
                locationY_5 = source1.location["y"] + random.randint(7,28)
                
        
        
                bezier_mouse_x_y(locationX_2, locationY_2, source1.size , panelHeight)
                time.sleep(float(random.uniform(.05, .3)))
                bezier_mouse_x_y(locationX_3, locationY_3, source1.size , panelHeight)
                time.sleep(float(random.uniform(.05, .3)))
                bezier_mouse_x_y(locationX_4, locationY_4, source1.size , panelHeight)
        
                bezier_mouse_x_y(locationX, locationY, source1.size , panelHeight)
        
                
                #pyautogui.move(difference, 0)
                
                pyautogui.mouseUp()
                bezier_mouse_x_y(locationX_5, locationY_5, source1.size , panelHeight)
                time.sleep(float(random.uniform(.05, .3)))
                resting_mouse()
                
                #time.sleep(10)
                #print("Starting WebdriverWait for exception 11")

                #Checking for image icon of an envelope that appears when account is created successfully // Checking for svg of an X when Network Error appears // Search for "Slide to complete the puzzle" if the puzzle is not solved sucesssfully
                #try:
                #    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div/img")) or EC.visibility_of_element_located((By.XPATH, "/div/div/svg")) or EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[1]")))
                #except Exception as ee:
                #    print(ee)
                #    print("Exception occured: 11")
                #    break
                
                accountCreated = 0
                accountCreatedCheckIterations = 0
                
                while accountCreated == 0:
                    time.sleep(0.5)
                    if "We've sent you an activation email" in driver.page_source:
                        
                        print("Captcha Solved!")
                        captcha_solved = 1
                        print("Account created!")
                        resting_mouse()
    
                        #Fetch emails from Yopmail
                        
                        '''
                        try:
                            driver.set_page_load_timeout(60)
                            url='https://yopmail.com/en/'
                            driver.get(url)
                        except Exception:
                            print('Page Loading forever, pressing ESC to stop loading')
                            pyautogui.press('esc')
                        
                        print("Activating Account... ")
            
                        #Close Allow Cookie popup if exists
                        
                        if driver.find_elements(By.XPATH, '//*[@id="accept"]'):
                            allowCookies = driver.find_element(By.XPATH,'//*[@id="accept"]')
                            bezier_mouse(allowCookies.location, allowCookies.size , panelHeight)
                            pyautogui.click()
            
                        resting_mouse()
                        
                        
                        #Add Email that I want to check
                        
                        try:
                            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]')))
                        except Exception:
                            print("Exception occured: 5")
                            break
                        
                        emailinput = driver.find_element(By.XPATH,'//*[@id="login"]')
                        bezier_mouse(emailinput.location, emailinput.size , panelHeight)
                        pyautogui.click()
                        slow_type(driver.find_element(By.XPATH,'//*[@id="login"]'),email)
                    
            
                        #Check Emails
                        
                        try:
                            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="refreshbut"]/button/i')))
                        except Exception:
                            print("Exception occured: 6")
                            break
                            
                        emailButton = driver.find_element(By.XPATH,'//*[@id="refreshbut"]/button/i')
                        bezier_mouse(emailButton.location, emailButton.size , panelHeight)
                        pyautogui.click()
                        resting_mouse()
                        time.sleep(5)
                        
                        
                        #Open Account Activation Link
                        
                        try:
                            WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="ifmail"]')))
                        except Exception:
                            print("Exception occured: 7")
                            break
        
                        verificationLink = driver.find_element(By.XPATH,'//*[@id="mail"]/div/div/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[7]/td/span/a')
                        
                        try:
                            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mail"]/div/div/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[7]/td/span/a')))
                        except Exception:
                            print("Exception occured: 8")
                            break
                                                
                        confirmation_link = driver.find_element(By.XPATH,'//*[@id="mail"]/div/div/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[7]/td/span/a').get_attribute('href')
                        driver.switch_to.default_content()
                        print(confirmation_link)
                        '''         
                        
                        
                        #Get link from Email to Activate Account
    
                        headers = CaseInsensitiveDict()
                        
                        
                        headers["Accept"] = 'application/vnd.mailcare.v1+json'
                        headers["Authorization"] = 'Basic c291b2RhdmlkZUBnbWFpbC5jb206MTIzNDVzb3VvZGF2aWRlIQ=='
                        
                        url = 'http://nomadside.com/api/emails?page=&limit=1&inbox='+str(email)+'&sender=&subject=&since=&until=&search=&unread=&favorite='
                        
                        resp = requests.get(url, headers=headers)
                        
                        response_body = resp.content
                        response_body = json.loads(response_body)
                        
                        
                        last_email_id = (response_body['data'][0]['id'])
                        
                        
                        headers = CaseInsensitiveDict()
                        
                        
                        headers["Accept"] = 'text/html'
                        headers["Authorization"] = 'Basic c291b2RhdmlkZUBnbWFpbC5jb206MTIzNDVzb3VvZGF2aWRlIQ=='
                        
                        url = 'https://nomadside.com/api/emails/'+str(last_email_id)
                        
                        resp = requests.get(url, headers=headers)
                        
                        response_body = str(resp.content)
                        confirmation_link = find_between( response_body, 'clicktracking="off" href="', '" class="es-button"' )
                        confirmation_link = confirmation_link.replace('amp;', '')
    
                        print(confirmation_link)
                        
                        try:
                            driver.set_page_load_timeout(60)
                            url=confirmation_link
                            driver.get(url)
                        except Exception:
                            print('Page Loading forever, pressing ESC to stop loading')
                            pyautogui.press('esc')
    
                        print("Account Activated!")
                        print("Searching for session token...")
                        
                        sessionfetched = 0
                        GetTokenRetryAmount = 0
                        while sessionfetched == 0:
                            for request in driver.requests:
                                
                                findThis = "Bearer"
                                
                                if findThis in str(request.headers):
                                    print("Session token found!")
                                    sessionToken = str(request.headers)
                                    sessionfetched = 1
                                    
                                    # Fetch just the authorization token (session) from the whole request header
                                    sub1 = "Bearer"
                                    sub2 = "content-type:"
                                    
                                    idx1 = sessionToken.index(sub1)
                                    idx2 = sessionToken.index(sub2)
                                    
                                    sessionToken = sessionToken[idx1 + len(sub1) + 1: idx2]
                                    
                                    sessionLocalStorage = driver.execute_script("return localStorage.getItem('u');")
                                    print(sessionLocalStorage+"\n")
                                    sessionLocalStorage = str(sessionLocalStorage)
                                    
                                    # Save Session to TXT files
                                    with open('sessions_full.txt', 'a') as file:
                                        dateNow = str(datetime.now())
                                        print(str(ip)+"          "+dateNow+"          "+"Email: "+email+"          "+password+"          "+sessionToken)
                                        file.write(str(ip)+"          "+dateNow+"          "+"Email: "+email+"          "+password+"          "+sessionToken)
                                        
                                    with open('sessions.txt', 'a') as file:
                                        file.write(sessionToken)            
                                        
                                    with open('sessions_selenium.txt', 'a') as file:
                                        file.write(sessionLocalStorage+'\n')
                                    
                                    # Save Session to MYSQL Database
                                    mydb = mysql.connector.connect( host="sql327.main-hosting.eu", user="u830852358_cmc", password="Davide74", database="u830852358_cmc")
                                    mycursor = mydb.cursor()
                                    
                                    sql = "INSERT INTO sessions (ip, email, password, session, session_selenium, date_created) VALUES (%s, %s, %s, %s, %s, %s)"
                                    val = (str(ip) , email, password, sessionToken, sessionLocalStorage, dateNow)
                                    mycursor.execute(sql, val)
                                    
                                    mydb.commit()
                                    print("Session saved into Database with ID: ", mycursor.lastrowid)
                                    
                                    print("############### ACCOUNT INFO AND COOKIE SAVED! ###############")


    
                                    # Rotate proxy after account is created
                                    url = "https://dashboard.iproyal.com/4g-mobile-proxies/rotate-ip/lithuanian/begVEeOcP"
                    
                                    payload={}
                                    headers = {
                                    'Content-Type': 'application/json'
                                    }
                                    
                                    response = requests.request("GET", url, headers=headers, data=payload)
                                    restart_script = 1
                                    print(response.text)
                                    print("Restarting and rotating proxy!")
                                    
                                    accountCreated = 1
                                    break
                                    
                            if sessionfetched == 0:
                                if GetTokenRetryAmount > 1:
                                    print("FAILED to get Session token, SKIPPING")
                                    accountCreated = 1
                                    break
                                    
                                    
                                GetTokenRetryAmount+=1
                                print("Session token not found, retrying.. x"+str(GetTokenRetryAmount))
                                
                                
                                
                                try:
                                    driver.set_page_load_timeout(60)
                                    url=confirmation_link
                                    driver.get(url)
                                except Exception:
                                    print('Page Loading forever, pressing ESC to stop loading')
                                    pyautogui.press('esc')
                        
                            
                    elif "Slide to complete the puzzle" in driver.page_source:
                        print("FAILED to solve Captcha!")
                        pyautogui.moveTo(random.randint(1600,1750), random.randint(400,850))  
                        pyautogui.click()
                        break
                    else:
                        accountCreatedCheckIterations+=1
                        if accountCreatedCheckIterations == 20:
                            print("ERROR")
                            network_error = 1
                            break
            driver.quit()
    

currentRunNumber = 0
quantityOfAccounts = 50000
    
#range is the number of exceptions it handles until it just doesnt try to run the main script again
for i in range(1, 5000):
    try:
        main(currentRunNumber,quantityOfAccounts)
    except Exception as e:
        print (e)
        print('#####################################################')
        print('UNKNOWN EXCEPTION OCCURED, Restarting main function!')
        print('#####################################################')
        continue
    else:
        break
    
    
    
    
    
    
    
    
    