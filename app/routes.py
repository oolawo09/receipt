from flask import url_for, render_template, redirect, request, \
    flash, session, make_response
from app import app, db
from app.forms import ReceiptForm, PreviewForm, LoginForm, \
    RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from app.models import User, Receipt, Item
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


@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
def index():
    form = ReceiptForm()

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
                           form=form)


@app.route('/preview', methods=['get', 'post'])
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
        

@app.route('/download', methods=['get', 'post'])
def download():
    if request.method == 'POST':
        return redirect(url_for('guide', code=200))
    return render_template('download.html')


@app.route('/guide', methods=['get'])
def guide():
    return render_template('guide.html')


@app.route('/sign_up', methods=['get', 'post'])
def sign_up():
    return "sign up"


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    receipts = user.receipts.order_by(Receipt.id).paginate(
        page, app.config['RECEIPTS_PER_PAGE'], False
    )
    next_url = url_for('user', username=user.username, page=receipts.next_num) \
        if receipts.has_next else None
    prev_url = url_for('user', username=user.username, page=receipts.prev_num) \
        if receipts.has_prev else None
    return render_template('user.html', user=user, receipts=receipts.items,
                            next_url=next_url, prev_url=prev_url)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)