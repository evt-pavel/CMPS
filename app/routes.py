import flask
from app import app, session
from flask import render_template, redirect, flash, request, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user
from app.models import User, Brand
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    brands = session.query(Brand).all()
    return render_template('index.html', title='WLCM T CMPS', brands=brands)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже авторизированы!')
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = session.query(User).filter_by(email=form.email.data).first()

        if user is None or user.check_password(form.password.data) == False:
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash('Loging success!')
        next_page = flask.request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form, title='Sign In')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash('Вы уже зарегистрированы и даже авторизированы!')
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():

        user = User()
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.generate_password(form.password.data)

        session.add(user)
        session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)


@app.route('/profile/<email>')
@login_required
def profile(email):
    user = session.query(User).filter_by(email=email).first()
    return render_template('profile.html', title='profile', user=user)


# @app.route('/admin')
# def admin():
#     brand = session.query(Brand).all()
#     return render_template('admin.html', bra)
