from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields import StringField, PasswordField
from wtforms.fields.html5 import DecimalField
from wtforms.validators import Length, email, EqualTo, DataRequired, URL, Optional
from yumroad.models import User

class ProductForm(FlaskForm):
    name = StringField('Name', [Length(min=4, max=60)])
    description = StringField('Description')
    picture_url = StringField('Picture URL', description='Optional', validators=[Optional(), URL()])
    price = DecimalField('Price', description='in USD, Optional', validators=[Optional()]) # Should this be optional???


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    store_name = StringField('Store Name', validators=[DataRequired(), Length(min=4)])


    def validate(self):
        check_validate = super(SignupForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('That email already has an account')
            return False

        return True

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user or not check_password_hash(user.password, self.password.data): # should be 'or'?
            self.email.errors.append('Invalid email or password')
            return False

        return True





