#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'todo_list.db')
db_url = f"sqlite:///{db_path}"

# Initialize Flask app
app = Flask(__name__)
secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'  # Use lowercase table name for consistency
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Task(db.Model):
    __tablename__ = 'tasks'  # Use lowercase table name for consistency
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Integer, default=0)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.title}>"

# Create database tables (only needed once)
with app.app_context():
    db.create_all()

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    return render_template('add-task.html')


if __name__ == '__main__':
    app.run(debug=True)
