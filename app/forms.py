from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import IntegerField, StringField, \
    FormField, DateField, TextAreaField
from wtforms.validators import DataRequired


class TelephoneForm(Form):
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    area_code = IntegerField('Area Code/Exchange', validators=[DataRequired()])
    number = StringField('Number')


class ContactDetailsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', )
    phone = FormField(TelephoneForm)


class OrderDetailsForm(FlaskForm):
    number = IntegerField('Number', validators=[DataRequired()])


class LineItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    rate = IntegerField('Rate', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    additional_details = TextAreaField('Additional details')


class ReceiptForm(FlaskForm):
    sender_details = FormField(ContactDetailsForm)
    recipient_details = FormField(ContactDetailsForm)
    order_details = FormField(OrderDetailsForm)
