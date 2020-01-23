from flask import render_template
from app import app
from app.forms import ContactDetailsForm, OrderDetailsForm


@app.route('/')
@app.route('/index')
def index():
    sender_form = ContactDetailsForm() 
    recipient_form = ContactDetailsForm()
    order_details_form = OrderDetailsForm()
    return render_template('receipt.html', sender_form=sender_form, recipient_form=recipient_form, order_details_form=order_details_form)