#!bin/user/python3
from morse_converter import *

# This script runs the Morse Converter Program

converter = MorseConverter()

is_on = True

while is_on:
    result = converter.convert()
    print(result)

    user_choice = input("Press 'q' to quit or 'c' to continue: ").strip().lower()

    if user_choice == "q":
        is_on = False
    elif user_choice == "c":
        continue
    else:
        print("Invalid input. Press 'q' to quit or 'c' to continue.")
