#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import secrets
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import TaskForm, RegistrationForm, LoginForm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'todo_list.db')
db_url = f"sqlite:///{db_path}"

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Bootstrap 5
Bootstrap5(app)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

# Models
class User(UserMixin, db.Model):
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

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
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
            return redirect(url_for('signin'))
        else:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))
    
    # Render the signup form
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if the user exists
        user = User.query.filter((User.username == username) | (User.email == email)).first()
        if user and check_password_hash(user.password, password):
            # User authenticated successfully
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Invalid credentials
            flash('Invalid username/email or password!', 'danger')
            return redirect(url_for('signin'))
    # Render the login form
    return render_template('signin.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Fetch all tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        completed = form.completed.data

        # Create new task
        new_task = Task(title=title, description=description, completed=completed, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add-task.html', form=form)

@app.route('/dashboard/<int:task_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(task_id):
    tasks = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if tasks:
        db.session.delete(tasks)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Task not found!', 'danger')
    return render_template('dashboard.html', user=current_user, tasks=tasks)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.completed = form.completed.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit-task.html', form=form, task=task)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out!', 'success')
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)
