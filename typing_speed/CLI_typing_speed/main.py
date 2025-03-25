#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import random

""" This script checks the typing speed of the user."""

text = None
user_input = None
text_choice = random.randint(1, 6)

if text_choice == 1:
    text_choice = "text1.txt"
elif text_choice == 2:
    text_choice = "text2.txt"
elif text_choice == 3:
    text_choice = "text3.txt"
elif text_choice == 4:
    text_choice = "text4.txt"
else:
    text_choice = "text5.txt"


def typing_speed(text_choice):
    """
    Checks the typing speed of the user
    :param text_choice:
    :print typing speed
    """
    print("Type the following text as fast as you can: \n")
    global text, user_input
    with open(text_choice, "r") as f:
        text = f.read()
    print(text)
    start_time = time.time()
    user_input = input()
    end_time = time.time()
    elapsed_time = end_time - start_time
    words = text.split()
    num_words = len(words)
    speed = num_words / elapsed_time
    print(f"Your typing speed is {speed:.2f} words per second.")


def check_accuracy(text, user_input):
    """
    Checks the typing accuracy of the user
    :param text:
    :param user_input:
    :print accuracy of the typing speed
    """
    text = text.upper().split()
    user_input = user_input.upper().split()
    correct = 0
    for i in range(len(text)):
        if i < len(user_input) and user_input[i] == text[i]:
            correct += 1
    accuracy = (correct / len(text))*100
    print(f"Your accuracy is {accuracy:.2f}%.")


def missing_words(text, user_input):
    """
    Return missing words
    :param text:
    :param user_input:
    :return: missing words
    """
    text = text.lower().split()
    user_input = user_input.lower().split()
    missing_words = []
    for i in range(len(text)):
        if i < len(user_input) and user_input[i] != text[i]:
            missing_words.append(text[i])
    print("Missing words:")
    print("Missing words {}".format(*missing_words, sep="\n"))


if __name__ == "__main__":
    typing_speed(text_choice)
    check_accuracy(text, user_input)
    missing_words(text, user_input)
