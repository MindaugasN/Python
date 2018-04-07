from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Vartojo vardas', validators=[DataRequired()])
    password = PasswordField('Slaptažodis', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class InvoiceForm(FlaskForm):
    name = StringField('Vardas', validators=[DataRequired()])
    surname = StringField('Pavardė', validators=[DataRequired()])
    email = StringField('Email')
    phone = StringField('Telefono nr.')
    address = StringField('Adresas')
    invoice_no = StringField('SF numeris', validators=[DataRequired()])
    purchase_1 = StringField('Prekė 1', validators=[DataRequired()])
    purchase_2 = StringField('Prekė 2')
    purchase_3 = StringField('Prekė 3')
    purchase_4 = StringField('Prekė 4')
    purchase_5 = StringField('Prekė 5')
    send = BooleanField('Siuntimas')
    submit = SubmitField('Vykdyti')
