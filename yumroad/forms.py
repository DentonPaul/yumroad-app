from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields import StringField, PasswordField
from wtforms.validators import Length, email, required, EqualTo
from yumroad.models import User

class ProductForm(FlaskForm):
    name = StringField('Name', [Length(min=4, max=60)])
    description = StringField('Description')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[email(), required()])
    password = PasswordField('Password', validators=[required(), Length(min=4), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[required()])

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
    email = StringField('Email', validators=[email(), required()])
    password = PasswordField('Password', validators=[required()])

    def validate(self):
        check_validate = super(SignupForm, slef).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user and not check_password_hash(user.password, self.password.data): # should be 'or'?
            self.email.errors.append('Invalid email or password')
            return False

        return True





