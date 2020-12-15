from flask import Blueprint, render_template, redirect, url_for, flash

from yumroad.extensions import db, login_manager
from yumroad.models import User
from yumroad.forms import SignupForm, LoginForm

from flask_login import login_user, current_user

user_bp = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        # create a user
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registered successfully", "success")
        return redirect(url_for('products.index'))
    return render_template('users/register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        return redirect(url_for('products.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # log in user
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)
        flash('Logged in successfully', 'success')
        return redirect(url_for('products.index'))
    return render_template('users/login.html', form=form)


