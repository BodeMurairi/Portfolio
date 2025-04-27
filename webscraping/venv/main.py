#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
This script collects data about top entrepreneurial leadership
books from theceolibrary and displays it to the user
'''


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def find_book_title(driver):
    books_element = driver.find_elements(By.CLASS_NAME, value="book-title")
    return [book.text for book in books_element]


def find_book_author(driver):
    book_info = driver.find_elements(By.CLASS_NAME, value="book-info")
    books_authors = [book.text for book in book_info]
    books_authors_name = []
    for i in books_authors:
        books_authors_name.append(i.replace("by", "").strip())
    return books_authors_name


def find_books_links(driver):
    element_books_links = driver.find_elements(
        By.CSS_SELECTOR,
        value='.fcl-entry .book-cover a'
    )
    return [element.get_attribute('href') for element in element_books_links]


def author_bio(driver):
    book_infos = driver.find_elements(By.CLASS_NAME, "book-info")
    author_links = []
    for info in book_infos:
        try:
            a_tag = info.find_element(By.TAG_NAME, "a")
            link = a_tag.get_attribute('href')
            author_links.append(link)
        except Exception:
            pass
    return author_links


def book_record(books, books_authors, books_links, author_bio_links):
    book_rec = []
    for book, author, link, bio in zip(
        books, books_authors, books_links, author_bio_links
    ):
        book_rec.append({
            "Book Name": book,
            "Author": author,
            "Link to Book": link,
            "Link to Author Bio": bio
        })
    return book_rec


def main():
    driver = setup_driver()
    driver.get("https://theceolibrary.com/")

    # Add sleep to allow page to load completely
    time.sleep(3)

    books = find_book_title(driver)
    books_authors = find_book_author(driver)
    books_links = find_books_links(driver)
    author_bio_links = author_bio(driver)

    books_record_list = book_record(
        books, books_authors, books_links, author_bio_links
    )

    while True:
        print("\nWelcome to our book recommendation system 📚✨")
        print("_________________________________________________")
        print("Here are the top recommended entrepreneurial"
              "leadership books:\n")

        for idx, book in enumerate(books_record_list):
            print(f"{idx + 1}. {book['Book Name']} by {book['Author']}")

        print("\nOptions:")
        print("1. View detailed info about a book")
        print("2. Exit")

        choice = input("\nEnter your choice (1 or 2): ")

        if choice == "1":
            try:
                selected = int(input(
                    "Enter the book number you want to know"
                    " more about: "
                ))
                selected_book = books_record_list[selected - 1]
                print("\n------------------------")
                print(f"Book Name: {selected_book['Book Name']}")
                print(f"Author: {selected_book['Author']}")
                print(f"Book Link: {selected_book['Link to Book']}")
                print(f"Author Bio Link: {selected_book['Link to Author Bio']
                                          }")
                print("------------------------\n")
            except (IndexError, ValueError):
                print("Invalid selection. Please try again.")

        elif choice == "2":
            print("Thank you for using our book recommendation system!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Close driver
    driver.quit()


if __name__ == "__main__":
    main()
