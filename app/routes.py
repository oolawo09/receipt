from flask import url_for, render_template, redirect, request, \
    flash
from app import app, db
from app.forms import ReceiptForm, PreviewForm, LoginForm, RegistrationForm
from app.models import User, Receipt, Item
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
def index():
    form = ReceiptForm()

    if form.validate_on_submit():
        receipt = Receipt()
        db.session.add(receipt)

        receipt.notes = form.notes.data
        receipt.recipient = form.recipient.data
        receipt.sender = form.sender.data

        for item in form.items.data:
            new_item = Item(**item)
            receipt.items.append(new_item)

        if current_user.is_authenticated:
            user = User.query.get(current_user.id)
            user.receipts.append(receipt)
            db.session.add(user)

        db.session.commit()

        return redirect(url_for('preview'), code=200)
    return render_template('receipt.html',
                           form=form)


@app.route('/preview', methods=['get', 'post'])
def preview():
    form = PreviewForm()
    if form.validate_on_submit(): 
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