from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ReceiptForm(FlaskForm):
    submit = SubmitField('Download')
      
