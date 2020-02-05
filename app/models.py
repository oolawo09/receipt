from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


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


class Receipt(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    recipient = db.Column(db.String(64))
    notes = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='receipt', lazy='dynamic',
                                 primaryjoin="Receipt.id == Item.receipt_id")

    def __repr__(self):
        return '<Receipt {}>'.format(self.notes)


class Item(db.Model):
    __tablename__ = 'line_item'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(64))
    quantity = db.Column(db.Integer)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.description)