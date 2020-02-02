from flask import url_for, render_template, redirect
from app import app
from app.forms import ReceiptForm


@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
@app.route('/create_receipt', methods=['get', 'post'])
def index():
    form = ReceiptForm()
    if form.validate_on_submit():
        return redirect(url_for('preview'), code=200)
    return render_template('receipt.html',
                           form=form)


@app.route('/preview', methods=['get', 'post'])
def preview():
    return render_template('preview.html')