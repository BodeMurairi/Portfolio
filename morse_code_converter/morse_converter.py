#!bin/user/python3
from morse_alphabet import morse_converter

# This class handles the Morse Convertion logic

class MorseConverter:
    def __init__(self):
        self.morse_converter = morse_converter
        self.reversed_dict = {value: key for key, value in self.morse_converter.items()}

    def convert(self):
        """Human to Morse Code """
        sentence = input("Enter a sentence that will be converted: ").upper()
        morse_code = " ".join(self.morse_converter.get(char, " ") for char in sentence)
        return morse_code

    def decode(self):
        """Converts Morse code to human text."""
        morse_code = input("Enter Morse code to be decoded: ").strip()

        # Split into words using "   " (three spaces)
        words = morse_code.split("   ")

        decoded_words = []
        for word in words:
            # Split into individual letters (single space) and decode them
            decoded_word = "".join(self.reversed_dict.get(char, "") for char in word.split())
            decoded_words.append(decoded_word)

        # Join words into a complete sentence
        return " ".join(decoded_words)
