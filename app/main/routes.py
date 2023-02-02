from app import scoped_session
from flask import render_template, redirect, flash, request, url_for
from app.main.forms import RegistrationOrder
from flask_login import current_user, login_required
from app.models import User, Part, ElementImage, Order, Basket
from datetime import datetime
from app.main import bp


@bp.get('/')
@bp.get('/index/')
def index():
    with scoped_session() as session:
        brands = session.query(Part).group_by(Part.brand_id)
        session.close()
    return render_template('main/index.html', title='WLCM T CMPS', brands=brands)


@bp.get('/profile/<id>')
@login_required
def profile(id):
    with scoped_session() as session:
        user = session.query(User).filter_by(id=id).first()
        orders = session.query(Order).filter_by(user_id=current_user.id).filter_by(status=1).all()
    return render_template('main/profile.html', title='profile', user=user, orders=orders)


@bp.get('/profile/order/<order_id>')
@login_required
def order(order_id):
    with scoped_session() as session:
        parts = session.query(Basket).filter_by(order_id=order_id).all()
        return render_template('main/order.html', parts=parts)


@bp.route('/<brand_name>/<brand_id>/type/', methods=['GET', 'POST'])
def type(brand_id, brand_name):
    with scoped_session() as session:
        parts = session.query(Part).filter_by(brand_id=brand_id).group_by(Part.type_id)
    return render_template('main/type.html', parts=parts)


@bp.get('/<brand_name>/<brand_id>/type/<type_id>/model/')
def model(brand_id, type_id, brand_name):
    with scoped_session() as session:
        parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
            .group_by(Part.model_id)
    return render_template('main/model.html', parts=parts)


@bp.get('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element')
def element(brand_name, brand_id, type_id, model_name, model_id):
    with scoped_session() as session:
        parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
            .filter(Part.model_id == model_id).group_by(Part.element_id)
    return render_template('main/element.html', parts=parts)


@bp.get('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element/<element_name>/<element_id>/'
           'part')
def part(brand_name, brand_id, type_id, model_name, model_id, element_name, element_id):
    with scoped_session() as session:
        parts = session.query(Part).filter(Part.brand_id == brand_id).filter(Part.type_id == type_id)\
            .filter(Part.model_id == model_id).filter(Part.element_id == element_id).group_by(Part.id)
        image = session.query(ElementImage).filter(ElementImage.model_id == model_id)\
            .filter(ElementImage.element_id == element_id).first() or {'url': 'element_images/default.jpeg'}
    return render_template('main/part.html', parts=parts, image=image)


@bp.route('/basket', methods=['GET', 'POST'])
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

        if order == None:
            basket = 'Корзина пуста!'
        else:
            basket = session.query(Basket).filter(Basket.order_id == order.id).group_by(Basket.part_id).all()
            if basket == []:
                basket = 'Корзина пуста!'
        return render_template('main/basket.html', basket=basket, form=form)


@bp.get('/addtobasket/<part_id>')
@login_required
def addToBasket(part_id):
    with scoped_session() as session:
        order = session.query(Order).filter_by(user_id=current_user.id).filter(Order.status == None).first()
        part = session.query(Part).get(part_id)

        if order == None:
            user = session.query(User).filter_by(id=current_user.id).first()
            order = Order(user=user)
            session.add(order)
            order = session.query(Order).filter_by(user_id=current_user.id).filter(Order.status == None).first()
            part_to_basket = Basket(order=order, part=part, amount=1)

        else:
            part_in_basket = session.query(Basket).filter_by(order_id=order.id).filter_by(part_id=part.id).first()

            if part_in_basket is None:
                    part_in_basket = Basket(amount=1, part=part, order=order)

            else:
                part_in_basket.amount = part_in_basket.amount + 1

        flash(part.description + ' добавлен(-а) в корзину!')

        return redirect(url_for('main.part', brand_name=part.brand.brand_name, brand_id=part.brand_id, type_id=part.type_id,
                                model_name=part.model.model_name, model_id=part.model_id, element_name=part.element.element_name,
                                element_id=part.element_id))


@bp.get('/deletefrombasket/<order_id>/<part_id>')
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
    return redirect(url_for('main.basket'))


