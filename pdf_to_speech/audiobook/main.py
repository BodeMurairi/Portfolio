#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from gtts import gTTS


def load_pdf():
    loader = PDFPlumberLoader("books/The Richest Man In Babylon ( PDFDrive ).pdf")
    # Load and split texts
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
        )
    documents = loader.load_and_split(text_splitter=splitter)
    return documents


# Convert text to audio
def text_to_audio(doc, language, file):
    """
    convert text to audio using gTTs
    """
    save_file = file + ".mp3"
    filename = os.path.join("books", save_file)
    
    # Check if doc is a list, then join the content of all pages
    if isinstance(doc, list):
        contents = ' '.join([page.page_content.strip() for page in doc])
    else:
        contents = doc.page_content.strip()

    tts = gTTS(text=contents, lang=language, slow=False)
    tts.save(filename)
    print(f"Audio saved as {filename}")

def main():
    """
    Main :
    """
    while True:
        print("Welcome to our audiobook generator!")
        print("We will convert the text to audio.")
        print("__________________________________________")
        file = input("Enter the name to save the file: ")
        language = input("Enter the language code (e.g., 'en' for English, 'en-uk' for British English, 'en-in' for Indian English): ")
        if language == "":
            print("No language code provided. Defaulting to English.")
            language = 'en'
        else:
            print(f"Language set to {language}")
        
        print("Please wait while we process the text...")
        
        # Call load_pdf() to get the document
        documents = load_pdf()
        
        # Pass the documents to text_to_audio
        text_to_audio(doc=documents, language=language, file=file)
        
        print("Audio conversion completed!")
        time.sleep(2)
        print("Exiting the program...")
        break

if __name__ == "__main__":
    main()
