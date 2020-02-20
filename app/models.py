from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login
from flask import session


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    receipts = db.relationship('Receipt', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Receipt(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    recipient = db.Column(db.String(64))
    notes = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='receipt', lazy='dynamic',
                                 primaryjoin="Receipt.id == Item.receipt_id")

    def add_receipt_to_session(receipt_form):
        session['receipt_notes'] = form.notes.data
        session['receipt_recipient'] = form.recipient.data
        session['receipt_sender'] = form.sender.data

    def __repr__(self):
        return '<Receipt {}>'.format(self.notes)
    
    def __init__(self, sender, recipient, notes, items):
        self.sender = sender
        self.recipient = recipient
        self.notes = notes

        for item in items:
            new_item = Item(**item)
            self.items.append(new_item)


class Item(db.Model):
    __tablename__ = 'line_item'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(64))
    quantity = db.Column(db.Integer)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'))

    def serialize(self):
        return {"id": self.id,
                "price": self.price,
                "description": self.description,
                "quantity": self.quantity}

    def __repr__(self):
        return '<Item {}>'.format(self.description)
