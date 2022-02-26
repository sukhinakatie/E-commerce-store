from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# модель для товаров
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50))
    details = db.Column(db.String)
    price = db.Column(db.Float)
    image_path = db.Column(db.String)


# модель для заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String)
    other = db.Column(db.String)


# модель для деталей заказа
# объекты модели определяют связь заказа с товаром, а также количество товара и его опцию (размер постера, ...)
# связь заказ-товар как один-много
class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    option = db.Column(db.String)


# данный код выполнится только в случае запуска именно этого скрипта (models.py) через консоль
# и нужен код только чтобы инициализировать базу данных - создать таблицы и наполнить тремя товарами
if __name__ == '__main__':
    from flask import Flask

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    db.init_app(app)
    with app.app_context():
        # создание таблиц для моделей, описанных выше
        db.create_all()

        # создание товаров

        poster_1 = Product(
            name='Moongirl Poster',
            details='''
            Printed Poster is an overwhelming choice of decoration!
            Forget about boring and repeatative designs. You can choose
            from a variety of sizes or even pick a digital download to
            print it yourself!<br>
            <br>
            ________________________________________________________<br>
            <br>
            Our posters are printed on a High-Quality Design Paper but if
            you want to decorate your space in an unusual way, we have 3
            alternative options for you. Just leave a comment during purchasing.
            -MARBLE PAPER
            -LINEN PAPER
            -WATERCOLOR PAPER
            ''',
            price=39,
            image_path='/static/img/poster_1.png',
        )

        poster_2 = Product(
            name='Mermaid Poster',
            details='''
            Printed Poster is an overwhelming choice of decoration!
            Forget about boring and repeatative designs. You can choose
            from a variety of sizes or even pick a digital download to
            print it yourself!<br>
            <br>
            ________________________________________________________<br>
            <br>
            Our posters are printed on a High-Quality Design Paper but if
            you want to decorate your space in an unusual way, we have 3
            alternative options for you. Just leave a comment during purchasing.
            -MARBLE PAPER
            -LINEN PAPER
            -WATERCOLOR PAPER
            ''',
            price=39,
            image_path='/static/img/poster_2.png',
        )

        poster_3 = Product(
            name='Shark Poster',
            details='''
            Printed Poster is an overwhelming choice of decoration!
            Forget about boring and repeatative designs. You can choose
            from a variety of sizes or even pick a digital download to
            print it yourself!<br>
            <br>
            ________________________________________________________<br>
            <br>
            Our posters are printed on a High-Quality Design Paper but if
            you want to decorate your space in an unusual way, we have 3
            alternative options for you. Just leave a comment during purchasing.
            -MARBLE PAPER
            -LINEN PAPER
            -WATERCOLOR PAPER
            ''',
            price=39,
            image_path='/static/img/poster_3.png',
        )

        case_1 = Product(
            name='Magic Case',
            details='''
            Case with a custom illustration is our top product! 
            Show off your uniqueness and style with this fascinating item.<br>
            <br>
            ________________________________________________________<br>
            <br>
            We use only professional systems to cover cases with illustrations. 
            All cases are made with soft touch cover, what makes them nice 
            to touch and hold as they are not slippery.
            ''',
            price=19,
            image_path='/static/img/case_1.png',
        )

        case_2 = Product(
            name='Wolf Case',
            details='''
            Case with a custom illustration is our top product! 
            Show off your uniqueness and style with this fascinating item.<br>
            <br>
            ________________________________________________________<br>
            <br>
            We use only professional systems to cover cases with illustrations. 
            All cases are made with soft touch cover, what makes them nice 
            to touch and hold as they are not slippery.
            ''',
            price=19,
            image_path='/static/img/case_2.png',
        )

        case_3 = Product(
            name='Tiger Case',
            details='''
            Case with a custom illustration is our top product! 
            Show off your uniqueness and style with this fascinating item.<br>
            <br>
            ________________________________________________________<br>
            <br>
            We use only professional systems to cover cases with illustrations. 
            All cases are made with soft touch cover, what makes them nice 
            to touch and hold as they are not slippery.
            ''',
            price=19,
            image_path='/static/img/case_3.png',
        )

        postcard_1 = Product(
            name='Sealife Postcard',
            details='''
            Forget about boring postcards! You can now choose from various of 
            pictures to make your celebration or wishes even more memorable.<br>
            <br>
            ________________________________________________________<br>
            <br>
            Postcards are goes with the standard size 148 x 105 cm. You can choose any paper 
            to print it on. Just leave a message while completing your order.
            ''',
            price=9,
            image_path='/static/img/postcard_1.png',
        )

        postcard_2 = Product(
            name='Forest Postcard',
            details='''
            Forget about boring postcards! You can now choose from various of 
            pictures to make your celebration or wishes even more memorable.<br>
            <br>
            ________________________________________________________<br>
            <br>
            Postcards are goes with the standard size 148 x 105 cm. You can choose any paper 
            to print it on. Just leave a message while completing your order.
            ''',
            price=9,
            image_path='/static/img/postcard_2.jpg',
        )

        postcard_3 = Product(
            name='Waterfall Postcard',
            details='''
            Forget about boring postcards! You can now choose from various of 
            pictures to make your celebration or wishes even more memorable.<br>
            <br>
            ________________________________________________________<br>
            <br>
            Postcards are goes with the standard size 148 x 105 cm. You can choose any paper 
            to print it on. Just leave a message while completing your order.
            ''',
            price=9,
            image_path='/static/img/postcard_3.jpg',
        )

        # сохранение их в базу данных
        db.session.add(poster_1)
        db.session.add(poster_2)
        db.session.add(poster_3)
        db.session.add(case_1)
        db.session.add(case_2)
        db.session.add(case_3)
        db.session.add(postcard_1)
        db.session.add(postcard_2)
        db.session.add(postcard_3)

        # применение изменений
        db.session.commit()
