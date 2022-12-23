from app import app
from flask import render_template, redirect, flash, request, url_for
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='WLCM T CMPS')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        flash('Loging success!')
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In')
