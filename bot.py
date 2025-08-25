from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from multiprocessing import Process
import argparse
import time
import random
import os

load_dotenv()

def attack():
    try:
        if args.install:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        else:
            browser = webdriver.Firefox()

        browser.get(args.url)

        botSteps(browser)
        
        browser.quit()
    except Exception as e:
        print(f"Error in attack: {e}")

def botSteps(browser):
        browser.find_element(By.LINK_TEXT, "About").click()

        browser.find_element(By.LINK_TEXT, "Home").click()

        previusElement = browser.find_element(By.ID, "controls-previus")
        nextElement= browser.find_element(By.ID, "controls-next")

        i=0
        while i < 7:
            if random.randint(1,2) == 1:
                nextElement.click()
            else:
                previusElement.click()
            i+=1

        browser.find_element(By.LINK_TEXT, "Login").click()

        time.sleep(1)

        #signup(browser, 1)

def signup(browser, times):
    browser.find_element(By.LINK_TEXT, "Sign Up").click()
    
    i=0
    while i < times:
        browser.execute_script(f"document.querySelector('#username').value='{random.randint(1,999)}'")
        browser.execute_script(f"document.querySelector('#password').value='changeme'")
        browser.execute_script(f"document.querySelector('#confirm-password').value='changeme'")

        solveCaptcha(browser)

        i += 1

def solveCaptcha(browser):
    if args.version == 2:
        clickCaptcha(browser)
    else:
        browser.find_element(By.XPATH, "//button[@type='submit']").click() 
    
    gRecaptchaResponse = ''

    while gRecaptchaResponse == '':
        gRecaptchaResponse = browser.execute_script("var elem = document.getElementById('g-recaptcha-response'); return elem ? elem.value : false;")
        time.sleep(1)
            
    if(not gRecaptchaResponse):
        print("Element 'g-recaptcha-response' not found!")
        browser.quit()
        exit()
    
    if args.version == 2:
        browser.execute_script("document.querySelector('#submit').click()")


parser = argparse.ArgumentParser()
parser.add_argument('-url', type=str, required=True, help='Target url. E.g: http://localhost/index.php')
parser.add_argument('-v', '--version', type=int, default=2, choices=[2, 3], help='Specify which version to use, available options are 2 or 3 (default: 2)')
parser.add_argument('-i', '--install', type=bool, default=False, help='Automatically download, install and configure the appropriate browser drivers (default: False)')
parser.add_argument('-P', '--process', type=int, default=1, help="Number of processes to spawn (default: 1).")
parser.add_argument('-d', '--delay', type=float, default=0.1, help="Delay between spawning processes in seconds (default: 0.1).")

args = parser.parse_args()

processes = []

for i in range(args.process):
    process = Process(target=attack, daemon=True)
    processes.append(process)
    process.start()

    time.sleep(args.delay)

for process in processes:
    if process.is_alive():
        process.join()
