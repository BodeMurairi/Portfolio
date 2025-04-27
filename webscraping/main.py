#!/usr/bin/env python3
from selenium import webdriver

'''
This script collects data about top entrepreneurial leadership books 
from theceolibrary and saves it to a pdf file
this file is sent to the user via email
'''
# Create a new driver instance
driver = webdriver.chrome()
# Open the URL
driver.get("https://theceolibrary.com/")
