#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import TaskForm, RegistrationForm
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

Bootstrap(app)
csrf = CSRFProtect(app)

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
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            # Check if the username or email already exists
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('Username or email already exists!', 'danger')
                return redirect(url_for('signup'))
            # Create new user
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            time.sleep(2)
            return redirect(url_for('signin'))
        else:
            flash('Passwords do not match!', 'danger')
            time.sleep(2)
            # Redirect to the signup page
            return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        email =  request.form["email"]
        password = request.form["password"]
        # Check if the user exists
        user = User.query.filter((User.username == username) | (User.email == email)).first()
        if user and check_password_hash(user.password, password):
            # User authenticated successfully
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials
            flash('Invalid username/email or password!', 'danger')
            time.sleep(2)
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    return render_template('add-task.html')


if __name__ == '__main__':
    app.run(debug=True)
