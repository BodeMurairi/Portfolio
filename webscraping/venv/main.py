#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
This script collects data about top entrepreneurial leadership books 
from theceolibrary and saves it to a pdf file
this file is sent to the user via email
'''

# Keep Chrome opened
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create a new driver instance
driver = webdriver.Chrome(options=chrome_options)

# Open the URL
driver.get("https://theceolibrary.com/")

# select books title
books_element = driver.find_elements(By.CLASS_NAME, value="book-title")
books = [book.text for book in books_element]


# select books author
book_info = driver.find_elements(By.CLASS_NAME, value="book-info")
books_authors = [book.text for book in book_info]

# Clean Author Name
books_authors_name = []
for i in books_authors:
    books_authors_name.append(i.replace("by","").strip())


# select books links
element_books_links = driver.find_elements(By.CSS_SELECTOR, value='.fcl-entry a')
books_links = [element.get_attribute('href') for element in element_books_links]

# Create a list to store book records
book_rec = []

# Combine book, author, and link together
for book, author, link in zip(books, books_authors_name, books_links):
    book_rec.append({
        "Book Name": book,
        "Author": author,
        "Link": link
    })

# Books recommandation per authors


# quit the driver
driver.quit()
