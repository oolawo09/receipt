from app import db


class Receipt(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64))
    recipient = db.Column(db.String(64))
    notes = db.Column(db.String(140))
    items = db.relationship('Item', backref='receipt', lazy='dynamic',
                                 primaryjoin="Receipt.id == Item.receipt_id")


class Item(db.Model):
    __tablename__ = 'line_item'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(64))
    quantity = db.Column(db.Integer)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'))