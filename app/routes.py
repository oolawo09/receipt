from flask import url_for, render_template, redirect
from app import app, db
from app.forms import ReceiptForm, PreviewForm
from app.models import Receipt, Item
from flask import request


@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
@app.route('/create_receipt', methods=['get', 'post'])
def index():
    form = ReceiptForm()

    if form.validate_on_submit():
        receipt = Receipt()
        db.session.add(receipt)

        for item in form.items.data:
            new_item = Item(**item)
            receipt.items.append(new_item)

        db.session.commit()

        return redirect(url_for('preview'), code=200)
    return render_template('receipt.html',
                           form=form)


@app.route('/preview', methods=['get', 'post'])
def preview():
    form = PreviewForm()
    if form.validate_on_submit(): 
        import pdb; pdb.set_trace()
        if form.download.data:
            return redirect(url_for('download'), code=200)
        if form.send_via_whatsapp.data:
            pass
    return render_template('preview.html', form=form)
        

@app.route('/download', methods=['get', 'post'])
def download():
    if request.method == 'POST':
        return redirect(url_for('guide', code=200))
    return render_template('download.html')


@app.route('/guide', methods=['get'])
def guide():
    return render_template('guide.html')