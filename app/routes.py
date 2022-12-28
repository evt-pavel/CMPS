from app import app, session
from flask import render_template, redirect, flash, request, url_for
from app.forms import LoginForm
from flask_login import login_user, current_user, login_required
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='WLCM T CMPS')


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
            redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Loging success!')
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In')
