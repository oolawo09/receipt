from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, \
    FormField, TextAreaField, FieldList, Form, \
    SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, \
    Email, EqualTo
from app.models import User


class LineItemForm(Form):
    price = IntegerField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class ReceiptForm(FlaskForm):
    sender = StringField('Sender', validators=[DataRequired()])
    recipient = StringField('Recipient', validators=[DataRequired()])
    items = FieldList(FormField(LineItemForm),
                      min_entries=0,
                      max_entries=20)
    notes = TextAreaField('Notes')


class PreviewForm(FlaskForm):
    download = SubmitField(label="download")
    send_via_whatsapp = SubmitField(label="send via whatsapp")