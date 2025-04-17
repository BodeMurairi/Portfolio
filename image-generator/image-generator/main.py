#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import secrets
import numpy as np
import webcolors
from PIL import Image
from sklearn.cluster import KMeans
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

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
    '''
    Form for uploading images.
    '''
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Images only!'),
            FileRequired('File field not uploaded!')
        ]
    )
    submit = SubmitField('Upload')


def closest_color(requested_color):
    """
    Function that finds the closest color name 
    to the requested RGB color.
    """
    min_colors = {}
    for name, hex_val in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors)]


# Route to serve uploaded files
@app.route('/uploads/<filename>')
def get_file_name(filename):
    '''
    Serve the uploaded file from the uploads directory.
    '''
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
    results = []

    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file_name', filename=filename)

        # Load and process image
        image_selected = Image.open(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
        # Resize image to 100x100 pixels
        image = image_selected.resize((100, 100))
        # Convert image to RGB
        image_np = np.array(image)
        # Flatten into 2D array
        pixels = image_np.reshape(-1, 3)

        # KMeans clustering to find dominant colors
        k = 10
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(pixels)
        dominant_colors = kmeans.cluster_centers_.astype(int)

        for color in dominant_colors:
            rgb = tuple(color)
            name = closest_color(rgb)
            # Convert numpy.int64 to native int
            rgb = tuple(int(x) for x in rgb)
            results.append({'rgb': rgb, 'name': name})

        return render_template('index.html', file_url=file_url, form=form, results=results)

    return render_template('index.html', file_url=file_url, form=form, results=results)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
