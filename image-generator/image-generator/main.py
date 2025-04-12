#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import secrets
from flask import Flask, request, render_template, jsonify, redirect, url_for, send_file
import numpy as np


# set up Flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

# set up flask roots

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
