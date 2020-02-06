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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')