from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Attiecība pret rezervācijām, lai varētu tās viegli atrast
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(50), unique=True, nullable=False) # Jaunais lauks
    status = db.Column(db.String(20), default="Pieejams")

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    # Lai parādītu datora nosaukumu rezervāciju tabulā
    computer = db.relationship('Computer', backref='reservations')
