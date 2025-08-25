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

        steps()
        
        browser.quit()
    except Exception as e:
        print(f"Error in attack: {e}")
def steps():
    time.sleep(5)
    
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
