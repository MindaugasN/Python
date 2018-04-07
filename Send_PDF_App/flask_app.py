from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# import pdfkit
from weasyprint import HTML, CSS
import datetime
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


from config import Config
from emailform import send_email
from forms import LoginForm
from forms import InvoiceForm





app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=('POST', 'GET'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    return render_template('login2.html', title='Sign In', form=form)

@app.route('/invoice', methods=('GET', 'POST'))
@login_required
def invoice():
    form = InvoiceForm()
    if form.validate_on_submit():
        return redirect(url_for('pdf_template'))
    return render_template('invoice_form2.html', title='SF online', form=form)


@app.route('/pdf_template', methods=('GET', 'POST')) # http://127.0.0.1/pdf_template
@login_required
def pdf_template():
    global name_g
    global surname_g
    global email_g
    global address_g
    global invoice_no_g
    global purchase_g
    global kiekis_g
    global kaina_g
    global suma_g
    global dict_g
    global bendra_suma_g
    global send_g
    global today_g



    name_g = request.form.get('name')
    surname_g = request.form.get('surname')
    email_g = request.form.get('email')
    address_g = request.form.get('address')
    invoice_no_g = request.form.get('invoice_no')
    purchase_g = request.form.getlist('purchase')
    kiekis_g = request.form.getlist('kiekis')
    kaina_g = request.form.getlist('kaina')
    suma_g = request.form.getlist('suma')
    bendra_suma_g = request.form.get('bendra_suma'),
    send_g = request.form.get('send') != None



    dict_g = dict(enumerate(zip(purchase_g, kiekis_g, kaina_g, suma_g)))

    today_g = datetime.datetime.now()
    today_g = today_g.strftime('%Y-%m-%d')
    # %Y-%m-%d

    return render_template(
        'pdf_template.html',
        name=name_g,
        surname=surname_g,
        email=email_g,
        address=address_g,
        invoice_no=invoice_no_g,
        dict_g=dict_g,
        bendra_suma_g = ('%.2f' % round(float(bendra_suma_g[0]), 2)),
        send=send_g,
        today=today_g
        )

@app.route('/pdf_send', methods=('GET', 'POST')) # http://127.0.0.1/pdf_template
@login_required
def pdf_send():


    rendered = render_template(
    'pdf_send2.html',
    name=name_g,
    surname=surname_g,
    email=email_g,
    address=address_g,
    invoice_no=invoice_no_g,
    dict_g=dict_g,
    bendra_suma_g = ('%.2f' % round(float(bendra_suma_g[0]), 2)),
    send=send_g,
    today=today_g
    )

    # css = ('app/static/style.css')
    # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    filename = 'SF-' + invoice_no_g +'.pdf'
    # pdfkit.from_string(rendered, filename, configuration = config, css=css)
    HTML(string=rendered).write_pdf(filename)
    send_email(filename, email_g)

    return redirect(url_for('index'))# redirect('http://www.islempos.eu', code=302)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))