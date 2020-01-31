from flask import url_for, render_template, redirect
from app import app
from app.forms import ContactDetailsForm, OrderDetailsForm


@app.route('/')
@app.route('/index', )
def index():
    return render_template('base.html')


@app.route('/sender_contact_form', methods=['get', 'post'])
def show_sender_contact_form():
    form = ContactDetailsForm()
    if form.validate_on_submit():
        return redirect(url_for('show_recipient_contact_form'), code=200)
    return render_template('sender_contact_details.html',
                           contact_form=form,
                           user="sender")


@app.route('/recipient_contact_form', methods=['get', 'post'])
def show_recipient_contact_form():
    form = ContactDetailsForm()
    if form.validate_on_submit():
        return redirect(url_for('show_receipt_details'), code=200)
    return render_template('recipient_contact_details.html',
                           contact_form=form,
                           user="recipient")


@app.route('/show_order_details_form', methods=['get', 'post'])
def show_order_details_form():
    form = OrderDetailsForm()
    if form.validate_on_submit():
        return redirect(url_for('show_preview'), code=200)
    return render_template('order_details.html',
                           order_form=form)


@app.route('/show_preview', methods=['get'])
def show_preview():
    return 'preview placeholder'
