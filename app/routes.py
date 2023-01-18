import flask
from app import app, session
from flask import render_template, redirect, flash, request, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user
from app.models import User, Part, ElementImage, Order, Basket
from werkzeug.urls import url_parse
from sqlalchemy import func


@app.route('/')
@app.route('/index/')
def index():
    brands = session.query(Part).group_by(Part.brand_id)
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


@app.route('/profile/<id>')
@login_required
def profile(id):
    user = session.query(User).filter_by(id=id).first()
    return render_template('profile.html', title='profile', user=user)


@app.route('/<brand_name>/<brand_id>/type/', methods=['GET', 'POST'])
def type(brand_id, brand_name):
    parts = session.query(Part).filter_by(brand_id=brand_id).group_by(Part.type_id)
    return render_template('type.html', parts=parts)


@app.route('/<brand_name>/<brand_id>/type/<type_id>/model/')
def model(brand_id, type_id, brand_name):
    parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
        .group_by(Part.model_id)
    return render_template('model.html', parts=parts)


@app.route('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element')
def element(brand_name, brand_id, type_id, model_name, model_id):
    parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
        .filter(Part.model_id == model_id).group_by(Part.element_id)
    return render_template('element.html', parts=parts)


@app.route('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element/<element_name>/<element_id>/'
           'part')
def part(brand_name, brand_id, type_id, model_name, model_id, element_name, element_id):
    parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
        .filter(Part.model_id == model_id).filter(Part.element_id == element_id).group_by(Part.id)
    image = session.query(ElementImage).filter(ElementImage.model_id == model_id)\
        .filter(ElementImage.element_id == element_id).first() or {'url': 'element_images/default.jpeg'}
    return render_template('part.html', parts=parts, image=image)


@app.route('/basket')
def basket():
    order = session.query(Order).filter(Order.user_id == current_user.id).filter(Order.status == 0).first()
    # добавить проверку есть ли уже созданный заказ или нет, если нет то создать
    basket = session.query(Basket).filter(Basket.order_id == order.id).group_by(Basket.part_id).all()
    return render_template('basket.html', basket=basket)


@app.route('/addtobasket/<part_id>')
@login_required
def addToBasket(part_id):

    order = session.query(Order).filter_by(user_id=current_user.id).filter(Order.status == 0).first()
    part = session.query(Part).get(part_id)
    if order == None:
        order = Order(user=current_user)
        session.add(order)
        session.commit()
        basket = Basket(amount=1, part=part, order=order)
        session.add(basket)
        session.commit()
    else:
        basket = session.query(Basket).filter_by(order_id=order.id).filter_by(part_id=part.id).first()

        if basket == None:
            basket = Basket(amount=1, part=part, order=order)
            session.add(basket)
            session.commit()
        else:
            basket.amount = basket.amount + 1
            session.commit()

        flash(part.description + ' добавлен(-а) в корзину!')

    return redirect(url_for('part', brand_name=part.brand.brand_name, brand_id=part.brand_id, type_id=part.type_id,
                     model_name=part.model.model_name, model_id=part.model_id, element_name=part.element.element_name,
                     element_id=part.element_id))


@app.route('/deletefrombasket/<order_id>/<part_id>')
def deleteFromBasket(order_id, part_id):

    part = session.query(Basket).filter_by(order_id=order_id).filter_by(part_id=part_id).first()
    # if part == None:
    #     description = 'Корзина пуста'

    if part.amount > 1:
        part.amount = part.amount - 1
        session.commit()
        description = part.part.description
    else:
        description = part.part.description
        session.query(Basket).filter_by(order_id=order_id).filter_by(part_id=part_id).delete()
        session.commit()

    flash(description + ' удален(-а)!')
    return redirect(url_for('basket'))


