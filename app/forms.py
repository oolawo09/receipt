from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, \
    FormField, DateField, TextAreaField
from wtforms.validators import DataRequired


class LineItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class ReceiptForm(FlaskForm):
    sender = StringField('Sender', validators=[DataRequired()])
    recipient = StringField('Recipient', validators=[DataRequired()])
    items = FormField(LineItemForm)
    notes = TextAreaField('Notes')