from app import session
from flask import render_template, redirect, flash, request, url_for
from app.main.forms import RegistrationOrder
from flask_login import current_user, login_required
from app.models import *
from datetime import datetime
from app.main import bp


@bp.get('/')
@bp.get('/index/')
def index():
    brands = session.query(Part).join(Model).join(Brand).group_by(Part.model_id).order_by(Brand.brand_name)
    return render_template('main/index.html', title='WLCM T CMPS', brands=brands)


@bp.get('/profile/<id>')
@login_required
def profile(id):
    user = session.query(User).filter_by(id=id).first()
    orders = session.query(Order).filter_by(user_id=current_user.id).filter_by(status=1).all()
    return render_template('main/profile.html', title='profile', user=user, orders=orders)


@bp.get('/profile/order/<order_id>')
@login_required
def order(order_id):
    parts = session.query(Basket).filter_by(order_id=order_id).all()
    return render_template('main/order.html', parts=parts)


@bp.route('/<brand_name>/<brand_id>/type/', methods=['GET', 'POST'])
def type(brand_id, brand_name):
    parts = session.query(Model).join(Brand).join(Part).filter(Model.brand_id == brand_id)
    return render_template('main/type.html', parts=parts)


@bp.get('/<brand_name>/<brand_id>/type/<type_id>/model/')
def model(brand_id, type_id, brand_name):
    parts = session.query(Model).join(Brand).join(Part).filter(Model.brand_id == brand_id)
    return render_template('main/model.html', parts=parts)


@bp.get('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element')
def element(brand_name, brand_id, type_id, model_name, model_id):
    parts = session.query(Part).filter_by(model_id=model_id).group_by(Part.element_id)

    return render_template('main/element.html', parts=parts)


@bp.get('/<brand_name>/<brand_id>/type/<type_id>/model/<model_name>/<model_id>/element/<element_name>/<element_id>/part')
def part(brand_name, brand_id, type_id, model_name, model_id, element_name, element_id):
    parts = session.query(Part).filter_by(model_id=model_id).filter_by(element_id=element_id)
    image = session.query(ElementImage).join(Element).join(Model).filter(Element.id == element_id).filter(Model.id == model_id).first()
    if image is None:
        image = 'element_images/default.jpeg'
    else:
        image = image.url
    return render_template('main/part.html', parts=parts, image=image)


@bp.route('/basket', methods=['GET', 'POST'])
def basket():
    form = RegistrationOrder(request.form)
    if request.method == 'POST' and form.validate():
        order = session.query(Order).filter_by(user=current_user).filter(Order.status == None).first()

        basket = session.query(Basket).filter_by(order=order).all()
        print(order.user.name, order.user.last_name)
        print('Адрес:', form.address.data)
        for b in basket:
            print(f'{b.id}. {b.part.part_number} {b.part.description} {b.amount} шт.')
        order.status = 1
        order.address = form.address.data
        order.date_order = datetime.utcnow()
        session.commit()
        flash('Заказ оформлен!')


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
    order = session.query(Order).filter_by(user_id=current_user.id).filter(Order.status == None).first()
    part = session.query(Part).get(part_id)

    if order == None:
        user = session.query(User).filter_by(id=current_user.id).first()
        order = Order(user=user)
        session.add(order)
        order = session.query(Order).filter_by(user_id=current_user.id).filter(Order.status == None).first()
        part_to_basket = Basket(order=order, part=part, amount=1)
        session.add(part_to_basket)
        session.commit()

    else:
        part_in_basket = session.query(Basket).filter_by(order_id=order.id).filter_by(part_id=part.id).first()

        if part_in_basket is None:
            part_to_basket = Basket(amount=1, part=part, order=order)
            session.add(part_to_basket)
            session.commit()

        else:
            part_in_basket.amount = part_in_basket.amount + 1
            session.commit()

    flash(part.description + ' добавлен(-а) в корзину!')

    return redirect(url_for('main.part', brand_name=part.model.brand.brand_name, brand_id=part.model.brand_id, type_id=part.model.type_id,
                            model_name=part.model.model_name, model_id=part.model_id, element_name=part.element.element_name,
                                element_id=part.element_id))


@bp.get('/deletefrombasket/<order_id>/<part_id>')
def deleteFromBasket(order_id, part_id):
    part = session.query(Basket).filter_by(order_id=order_id).filter_by(part_id=part_id).first()

    if part.amount > 1:
        part.amount = part.amount - 1
        description = part.part.description
        session.commit()
    else:
        description = part.part.description
        session.query(Basket).filter_by(order_id=order_id).filter_by(part_id=part_id).delete()
        session.commit()

    flash(description + ' удален(-а)!')
    return redirect(url_for('main.basket'))


