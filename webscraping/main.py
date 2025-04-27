#!/usr/bin/env python3
from selenium import webdriver

'''
This script collects data about top entrepreneurial leadership books 
from theceolibrary and saves it to a pdf file
this file is sent to the user via email
'''

# Keep Chrome opened
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('detach', True)

# Create a new driver instance
driver = webdriver.Chrome(options=chrome_options)
# Open the URL
driver.get("https://theceolibrary.com/")
