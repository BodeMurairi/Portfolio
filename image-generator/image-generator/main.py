#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import secrets
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from PIL import Image

# Set up Flask app
app = Flask(__name__)

# Secret key for CSRF protection
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Define the upload folder path
upload_folder = os.path.join(app.root_path, 'uploads', 'photos')

# Ensure the upload directory exists
os.makedirs(upload_folder, exist_ok=True)

# Configure the upload destination for the 'photos' UploadSet
app.config['UPLOADED_PHOTOS_DEST'] = upload_folder

# Set up photo upload set
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Form for uploading files
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Images only!'),
            FileRequired('File field not uploaded!')
        ]
    )
    submit = SubmitField('Upload')

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def get_file_name(filename):
    file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return "File not found", 404
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

# Index route for uploading and displaying images
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    file_url = None
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file_name', filename=filename)
    
    # Load the image if a file was uploaded
    image_selected = Image.open(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)).convert("RGB") if file_url else None
    image_array = np.array(image_selected)


    return render_template('index.html', file_url=file_url, form=form)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
