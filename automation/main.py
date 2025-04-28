#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

'''
This script automates the dinosaur game on elgoog.im using Selenium.
'''


# Set up the Chrome driver with options
chrome_options = Options()
chromr_options.chrome_options.add_experimental_option("detach", True)

# setup the chrome driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://elgoog.im/dinosaur-game/?bot")

driver.quit()
