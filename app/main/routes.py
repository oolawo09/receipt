from flask import url_for, render_template, redirect, request, \
    flash, session, make_response
from app import app, db
from app.main import bp
from app.main.forms import ReceiptForm, PreviewForm, LineItemForm
from app.main.models import User, Receipt, Item
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import pdfkit


def add_receipt_to_session(receipt_form):
    """
        :param receipt_form: A wtf_form instance
    """
    session['receipt_notes'] = receipt_form.notes.data
    session['receipt_recipient'] = receipt_form.recipient.data
    session['receipt_sender'] = receipt_form.sender.data
    session['receipt_items'] = receipt_form.items.data


def get_receipt_from_session():
    """
        :return receipt_form: A wtf_form instance
    """
    receipt = ReceiptForm()
    receipt.notes = session['receipt_notes']
    receipt.recipient = session['receipt_recipient']
    receipt.sender = session['receipt_sender']
    receipt.items = session['receipt_items']
    return receipt


@bp.route('/', methods=['get', 'post'])
@bp.route('/index', methods=['get', 'post'])
def index():
    form = ReceiptForm()
    lif = LineItemForm()

    if form.validate_on_submit():
        add_receipt_to_session(form)

        receipt = Receipt(sender=form.sender.data,
                          recipient=form.recipient.data,
                          notes=form.notes.data, items=form.items.data)
        db.session.add(receipt)

        if current_user.is_authenticated:
            user = User.query.get(current_user.id) 
            user.receipts.append(receipt)
            db.session.add(user)
        
        db.session.commit()

        return redirect(url_for('preview'), code=302)
    return render_template('receipt.html',
                           form=form, lif=lif)


@bp.route('/preview', methods=['get', 'post'])
def preview():
    form = PreviewForm()
    receipt = get_receipt_from_session()
    
    data = {
        "form": form, 
        "receipt": receipt
    }

    if form.validate_on_submit(): 
        if form.download.data:
            rendered = render_template('actual_preview.html', data=data)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['Content-Type'] = "application/pdf"
            response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
            return response
        if form.send_via_whatsapp.data:
            pass
 
    return render_template('preview.html', data=data)
        

@bp.route('/download', methods=['get', 'post'])
def download():
    if request.method == 'POST':
        return redirect(url_for('guide', code=200))
    return render_template('download.html')


@bp.route('/guide', methods=['get'])
def guide():
    return render_template('guide.html')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    receipts = user.receipts.order_by(Receipt.id).paginate(
        page, app.config['RECEIPTS_PER_PAGE'], False
    )
    next_url = url_for('main.user', username=user.username, page=receipts.next_num) \
        if receipts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=receipts.prev_num) \
        if receipts.has_prev else None
    return render_template('user.html', user=user, receipts=receipts.items,
                            next_url=next_url, prev_url=prev_url)