import flask
from app import app, scoped_session
from flask import render_template, redirect, flash, request, url_for
from app.forms import LoginForm, RegistrationForm, RegistrationOrder
from flask_login import login_user, current_user, login_required, logout_user
from app.models import User, Part, ElementImage, Order, Basket
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index/')
def index():
    with scoped_session() as session:
        brands = session.query(Part).group_by(Part.brand_id)
        session.close()
    return render_template('index.html', title='WLCM T CMPS', brands=brands)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже авторизированы!')
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        with scoped_session() as session:
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

        with scoped_session() as session:
            user = User()
            user.name = form.name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.generate_password(form.password.data)
            session.add(user)

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)


@app.route('/profile/<id>')
@login_required
def profile(id):
    with scoped_session() as session:
        user = session.query(User).filter_by(id=id).first()
    return render_template('profile.html', title='profile', user=user)


@app.route('/<brand_name>/<brand_id>/type/', methods=['GET', 'POST'])
def type(brand_id, brand_name):
    with scoped_session() as session:
        parts = session.query(Part).filter_by(brand_id=brand_id).group_by(Part.type_id)
    return render_template('type.html', parts=parts)


@app.route('/<brand_name>/<brand_id>/type/<type_id>/model/')
def model(brand_id, type_id, brand_name):
    with scoped_session() as session:
        parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
            .group_by(Part.model_id)
    return render_template('model.html', parts=parts)


@app.route('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element')
def element(brand_name, brand_id, type_id, model_name, model_id):
    with scoped_session() as session:
        parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
            .filter(Part.model_id == model_id).group_by(Part.element_id)
    return render_template('element.html', parts=parts)


@app.route('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element/<element_name>/<element_id>/'
           'part')
def part(brand_name, brand_id, type_id, model_name, model_id, element_name, element_id):
    with scoped_session() as session:
        parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
            .filter(Part.model_id == model_id).filter(Part.element_id == element_id).group_by(Part.id)
        image = session.query(ElementImage).filter(ElementImage.model_id == model_id)\
            .filter(ElementImage.element_id == element_id).first() or {'url': 'element_images/default.jpeg'}
    return render_template('part.html', parts=parts, image=image)


@app.route('/basket', methods = ['GET', 'POST'])
def basket():
    form = RegistrationOrder(request.form)
    if request.method == 'POST' and form.validate():
        with scoped_session() as session:
            order = session.query(Order).filter_by(user=current_user).filter(Order.status == None).first()

            basket = session.query(Basket).filter_by(order=order).all()
            print(order.user.name, order.user.last_name)
            print('Адрес:', form.address.data)
            for b in basket:
                print(f'{b.id}. {b.part.part_number} {b.part.description} {b.amount} шт.')
            order.status = 1
            order.address = form.address.data
            order.date_order = datetime.utcnow()

    with scoped_session() as session:
        order = session.query(Order).filter(Order.user_id == current_user.id).filter(Order.status == None).first()
    # добавить проверку есть ли уже созданный заказ или нет, если нет то создать

        if order == None:
            basket = 'Корзина пуста!'
        else:
            basket = session.query(Basket).filter(Basket.order_id == order.id).group_by(Basket.part_id).all()
        return render_template('basket.html', basket=basket, form=form)


@app.route('/addtobasket/<part_id>')
@login_required
def addToBasket(part_id):
    with scoped_session() as session:
        order = session.query(Order).filter_by(user_id=current_user.id).filter(Order.status == None).first()
        part = session.query(Part).get(part_id)

        if order == None:
            user = session.query(User).filter_by(id=current_user.id).first()
            order = Order(user=user)
            session.add(order)
            order = session.query(Order).get(2)
            part_to_basket = Basket(order=order, part=part, amount=1)

        else:
            part_in_basket = session.query(Basket).filter_by(order_id=order.id).filter_by(part_id=part.id).first()

            if part_in_basket == None:
                    part_in_basket = Basket(amount=1, part=part, order=order)

            else:
                part_in_basket.amount = part_in_basket.amount + 1

        flash(part.description + ' добавлен(-а) в корзину!')

        return redirect(url_for('part', brand_name=part.brand.brand_name, brand_id=part.brand_id, type_id=part.type_id,
                                model_name=part.model.model_name, model_id=part.model_id, element_name=part.element.element_name,
                                element_id=part.element_id))


@app.route('/deletefrombasket/<order_id>/<part_id>')
def deleteFromBasket(order_id, part_id):
    with scoped_session() as session:
        part = session.query(Basket).filter_by(order_id=order_id).filter_by(part_id=part_id).first()

        if part.amount > 1:
            part.amount = part.amount - 1
            description = part.part.description
        else:
            description = part.part.description
            session.query(Basket).filter_by(order_id=order_id).filter_by(part_id=part_id).delete()

    flash(description + ' удален(-а)!')
    return redirect(url_for('basket'))


