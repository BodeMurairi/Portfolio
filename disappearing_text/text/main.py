#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///disappearing_text.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
Base = declarative_base()
engine = create_engine('sqlite:///disappearing_text.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define the database model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def has_expired(self):
        return datetime.utcnow() > self.expires_at

# Create the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Save the message if it exists
    if request.method == 'POST':
        text = request.form.get('content')
        expires_in = int(request.form.get('expires_in', 10))
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        if text:
             new_message = Message(text=text, expires_at=expires_at)
             db.session.add(new_message)
             db.session.commit()
        return redirect(url_for('index'))

    # Retrieve non-expired messages
    messages = Message.query.filter(Message.expires_at > datetime.utcnow()).all()
    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
