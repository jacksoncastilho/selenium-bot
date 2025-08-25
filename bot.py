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

        browser.get(os.getenv('TARGET'))

        steps(browser)
        
        browser.quit()
    except Exception as e:
        print(f"Error in attack: {e}")

def steps(browser):
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

        signup(browser, 1)

        browser.find_element(By.LINK_TEXT, "Login").click()

        time.sleep(1)
        
        browser.find_element(By.ID, "username").send_keys(f"{random.randint(1,999)}")

        browser.find_element(By.ID, "password").send_keys("changeme")

        solveCaptchaV2(browser)

        signup(browser, 3)

def signup(browser, times):
    i=0
    while i < times:
        browser.find_element(By.LINK_TEXT, "Sign Up").click()

        browser.execute_script(f"document.querySelector('#username').value='{random.randint(1,999)}'")
        browser.execute_script(f"document.querySelector('#password').value='changeme'")
        browser.execute_script(f"document.querySelector('#confirm-password').value='changeme'")

        solveCaptchaV2(browser)

        i += 1

def solveCaptchaV2(browser):
    if os.getenv('RECAPTCHA_VERSION') == "v2" or os.getenv('RECAPTCHA_VERSION') == "both":
        clickCaptchaV2(browser)
        gRecaptchaResponse = ''

        while gRecaptchaResponse == '':
            gRecaptchaResponse = browser.execute_script("var elem = document.getElementById('g-recaptcha-response'); return elem ? elem.value : false;")
            time.sleep(1)
                
        if(not gRecaptchaResponse):
            print("Element 'g-recaptcha-response' not found!")
            browser.quit()
            exit()

    browser.find_element(By.XPATH, "//button[@type='submit']").click()         

def clickCaptchaV2(browser):
    try:
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']"))
        )

        checkbox = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        )

        checkbox.click()
    finally:
        browser.switch_to.default_content()

parser = argparse.ArgumentParser()
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
