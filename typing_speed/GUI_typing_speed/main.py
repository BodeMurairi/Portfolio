#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
from tkinter import *
from tkinter import scrolledtext

"""
This script checks the typing speed of the user using a GUI.
"""

# Function implementations

# Load the text


def load_text():
    global text_choice
    text_choice = random.choice(
        [
            "text1.txt",
            "text2.txt",
            "text3.txt",
            "text4.txt",
            "text5.txt",
            "text6.txt",
            "text7.txt",
            "text8.txt",
            "text9.txt",
            "text10.txt",
        ]
    )
    with open(text_choice, "r") as file:
        return file.read()


# Start the test
def start_test():
    global start_time, text, text_display, user_input

    # Clear previous test content
    if text_display:
        text_display.destroy()
    if user_input:
        user_input.destroy()

    # Load new test text
    text = load_text()
    start_time = time.time()

    # Create and display the new text
    text_display = Label(
        window,
        text=text,
        wraplength=580,
        justify="left",
    )
    text_display.pack(padx=10)
    user_input = scrolledtext.ScrolledText(
        window,
        wrap=WORD,
        width=70,
        height=10,
        state=NORMAL,
    )
    user_input.pack(pady=10)

    # Focus on the user input field
    user_input.focus_set()

    # Disable the start button to prevent multiple test starts
    start_button.config(state=DISABLED)


# Function to end typing and calculate speed and accuracy
def end_test():
    global end_time, typed_text
    end_time = time.time()
    elapsed_time = end_time - start_time
    typed_text = user_input.get(1.0, END).strip()
    user_input.config(state=DISABLED)
    start_button.config(state=NORMAL)

    # Calculate words per minute
    original_text = text.split()
    typed_words = typed_text.split()
    word_count = len(typed_words)
    wpm = (word_count / elapsed_time) * 60

    # Calculate accuracy
    count = 0
    for i in range(len(original_text)):
        if i < len(typed_words) and typed_words[i] == original_text[i]:
            count += 1
    accuracy = (count / len(original_text)) * 100

    # Display results
    result_label.config(
        text=f"Speed: {wpm:.2f} Words Per Minute\nAccuracy: {accuracy:.2f}%"
    )


def missing_words():
    global text, typed_text
    original_words = text.lower().split()
    typed_words = typed_text.lower().split()
    missing_words_list = []

    # Iterate through the original text and compare with typed words
    for i in range(len(original_words)):
        # If there are more words in the original text than typed words
        if i >= len(typed_words) or original_words[i] != typed_words[i]:
            missing_words_list.append(original_words[i])

    # Update the label to display missing words
    if missing_words_list:
        missing_word_text = "Missing words:\n" + "\n".join(missing_words_list)
    else:
        missing_word_text = "No missing words."

    result_label.config(text=f"You missed {len(missing_words_list)} words")


# UI setup

# Create the main window
window = Tk()
window.title("Typing Speed")
window.geometry("600x400")

# Load and display test
text = load_text()
text_display = Label(
    window,
    text=text,
    wraplength=580,
    justify="left",
)
text_display.pack(padx=10)

# Create a scrolled text widget for user input
user_input = scrolledtext.ScrolledText(
    window,
    wrap=WORD,
    width=70,
    height=10,
    state=DISABLED,
)
user_input.pack(pady=10)

# Create a frame for buttons
button_frame = Frame(window)
button_frame.pack(pady=10)

# Start button
start_button = Button(
    button_frame,
    text="Start Test",
    command=start_test,
)
start_button.grid(row=0, column=0, padx=5)

# End button
end_button = Button(
    button_frame,
    text="End Test",
    command=end_test,
)
end_button.grid(row=0, column=1, padx=5)

# Missing word button
missing_word_button = Button(
    button_frame,
    text="Missing Words",
    command=missing_words,
)
missing_word_button.grid(row=0, column=2, padx=5)

# Label to display results
result_label = Label(window, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Run the application
if __name__ == "__main__":
    window.mainloop()
