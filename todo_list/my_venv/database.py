#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
from sqlalchemy import SQLAlchemy, create_engine, String, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'todo_list.db')
db_url = f"sqlite:///{db_path}"
engine = create_engine(db_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
# Initialize SQLAlchemy
db = SQLAlchemy()

# Flask app configuration
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(200), nullable=False)

    task = relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Task(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Integer, default=0)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.title}>"
