#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os


def load_image():
    '''
    Load an image from the file system and display it on the canvas.
    '''
    global img, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))


def add_watermark():
    '''
    Add a watermark to the loaded image and display it on the canvas.
    '''
    if img:
        watermark_text = watermark_entry.get()
        editable_img = img.copy()
        draw = ImageDraw.Draw(editable_img)
        font_path = "SourceCodePro-Regular.ttf"  # Ensure this font file is accessible
        font_size = 36
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            print(f"Font '{font_path}' not found. Using default font.")
            font = ImageFont.load_default()
        
        # Calculate text size using textbbox
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        width, height = editable_img.size
        x, y = width - text_width - 10, height - text_height - 10
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
        
        img_display_watermarked = ImageTk.PhotoImage(editable_img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display_watermarked)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
        editable_img.save("watermarked_image.png")


# UI setup
# Create the main window
root = tk.Tk()
root.title("My Image Watermarking Application")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create the widgets
load_button = tk.Button(frame, text="Load Image", command=load_image)
load_button.grid(row=0, column=0, padx=5, pady=5)

# Create a label and an entry widget for the watermark text
watermark_label = tk.Label(frame, text="Watermark Text:")
watermark_label.grid(row=1, column=0, padx=5, pady=5)

# Create an entry widget for the watermark text
watermark_entry = tk.Entry(frame)
watermark_entry.grid(row=1, column=1, padx=5, pady=5)

# Create a button to apply the watermark
apply_button = tk.Button(frame, text="Apply Watermark", command=add_watermark)
apply_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Create a canvas to display the images
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(padx=10, pady=10)

img = None
img_display = None

root.mainloop()
