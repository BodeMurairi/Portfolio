#!/usr/bin/env python3
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import ImageGrab

'''
This script automates the dinosaur game on elgoog.im using Selenium.
'''


# Set up the Chrome driver with options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# setup the chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Wait 3 seconds so you can click into the game window
print("Get ready! Starting in 3 seconds...")
time.sleep(3)

driver.get("https://elgoog.im/dinosaur-game/?bot")

# Find the size of the screen
screen_width, screen_height = pyautogui.size()

pyautogui.click(x=960, y=540)
pyautogui.press('space')

box = (400, 400, 500, 500)

# Grab image from the screen
image = ImageGrab.grab(bbox=box)

# get the pixel data
pixel_data = image.getdata()

while True:
    for pixel in pixel_data:
        # Finding black with pixel (R, G, B)
        if pixel[0] < 100 and pixel[1] < 100 and pixel[2] < 100:
            # Found a dark pixel
            print("Obstacle detected!")
            break
