from flask import Flask, render_template, request, session, redirect, url_for

from forms import CheckoutForm
from models import db, Product, Order, OrderDetails

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_key'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db.init_app(app)


# '/' - по такому относительному пути будет доступна страница
# например, http://localhost:5000/
@app.route('/')
def main_page_view():
    """
    Отображение главной страницы
    """
    return render_template('main_page.html')


# страница доступна по адресу, http://localhost:5000/store
@app.route('/store')
def store_page_view():
    """
    Отображение страницы с товарами
    """

    products = Product.query.all()
    return render_template('store.html', products=products)


def add_to_cart(session, product_id, form):
    """
    Добавление товара в корзину. Бекенд запоминает состояние корзины через сессию (flask.session).
    Данный метод add_to_cart записывает в сессию товар, его количество и опцию.
    Вызывается со страниц для Постера, Кейса и Открытки.
    """

    cart = session.get('cart', [])
    cart.append({
        'id': product_id,
        'option': form.get('option', ''),
        'quantity': form.get('quantity', 1),
    })
    session['cart'] = cart


# methods=['GET', 'POST'] говорит о том, что этот метод принимает GET и POST запросы
# если не указать, по умолчанию методы принимают только GET запросы и отклоняют остальные
@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_view(product_id):
    """
    Отображение страницы с товаром
    """

    # получаем товар Постер из базы данных по ID
    product = Product.query.filter_by(id=product_id).first()

    # меняем опции и breadcrumbs в зависимости от типа товара
    if product_id in [1, 2, 3]:
        # товар - постер

        breadcrumbs = 'Store / Posters / ' + product.name.split()[0]
        options = [
            '50x70',
            '45x60',
            '35x50',
            'e-print',
        ]
        option_placeholder = 'Select Size'
    elif product_id in [4, 5, 6]:
        # товар - кейс

        breadcrumbs = 'Store / Cases / ' + product.name.split()[0]
        options = [
            'iPhone X',
            'iPhone XR',
            'iPhone 11',
            'iPhone 12',
        ]
        option_placeholder = 'Select Model'
    else:
        # товар - открытка

        breadcrumbs = 'Store / Postcards / ' + product.name.split()[0]
        options = [
            'A5',
            'A6',
            'A7',
        ]
        option_placeholder = 'Select Size'

    # если нажата кнопка Add to card, то происходит POST запрос на этот же адрес (напр. http://localhost:5000/product/?)
    # но в запросе передаются данные. Эти данные (товар, кол-во и опцию) мы записываем в сессию.
    if request.method == 'POST':
        add_to_cart(session, product.id, request.form)

    # после указания HTML шаблона (product.html), перечисляем переменные
    # в данном случае, например, Flask заменит участки в product.html вида {{ breadcrumbs }}
    # на 'Store / ??? / ???' и т.д.
    return render_template(
        'product.html',
        breadcrumbs=breadcrumbs,
        product=product,
        options=options,
        option_placeholder=option_placeholder,
    )


@app.route('/cart', methods=['GET', 'POST'])
def cart_view():
    # используем initial_data для того, чтобы когда человек допустил ошибки в форме (не заполнил какое-нибудь поле,
    # например), то ранее введенные данные не будут сброшены
    initial_data = {}

    # сформируем корзину на основе сессии
    products_data = []
    for item in session.get('cart', []):
        product = Product.query.filter_by(id=item['id']).first()
        products_data.append({
            'product': product,
            'quantity': item['quantity'],
            'option': item['option'],
        })

    # форма для чекаута. Та, что справа на странице.
    form = CheckoutForm(meta={'csrf': False})

    # если пользователь отправляет форму, т.е. нажата кнопка Pay
    if request.method == 'POST':
        # если в правой форме нет ошибок
        if form.validate():
            # далее пересчитаем указанное кол-во товаров, поскольку можно на странице с товаром
            # добавить в корзину 1 экземпляр, а на странице с чекаутом изменить кол-во и нажать Pay.
            # Таким образом будет сформирован заказ с тем кол-вом, для каждого товара, которое указано при чекауте
            quantities = [item for item in request.form if item[:9] == 'quantity_']
            for quantity in quantities:
                index = int(quantity[9:])
                products_data[index]['quantity'] = request.form[quantity]

            # создаем новый заказ и добавляем его в базу данных
            new_order = Order(
                first_name=form.first_name.data,
                surname=form.surname.data,
                email=form.email.data,
                address=form.address.data,
                other=form.other.data,
            )
            db.session.add(new_order)
            db.session.commit()

            # для каждого товара в корзине создадим деталь заказа, указав товар, детали, а также сам заказ
            for product_data in products_data:
                new_order_details = OrderDetails(
                    order_id=new_order.id,
                    product_id=product_data['product'].id,
                    quantity=product_data['quantity'],
                    option=product_data['option'],
                )
                db.session.add(new_order_details)

            db.session.commit()

            # очистим корзину
            session.pop('cart')

            # перенаправление на главную страницу
            return redirect(url_for('main_page_view'))
        else:
            # в форме есть ошибки. Отобразим на странице частично заполненную форму
            initial_data = {
                'first_name': form.first_name.data,
                'surname': form.surname.data,
                'email': form.email.data,
                'address': form.address.data,
                'other': form.other.data,
            }

    return render_template('cart.html', products_data=products_data, form=form, initial_data=initial_data)


@app.route('/cart/<int:product_index>/delete')
def delete_product(product_index):
    """
    Метод, вызываемый при нажатии на Крестик на странице с чекаутом. Удаляет товар из корзины.
    В метод поступает индекс товара в корзине (массиве) product_index, по которому однозначно можно понять,
    что нужно удалить
    """

    cart = session.get('cart', [])
    cart.pop(product_index)
    session['cart'] = cart
    return redirect(url_for('cart_view'))


if __name__ == '__main__':
    # запуск сервера
    app.run(debug=True)
