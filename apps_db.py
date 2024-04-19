from app import db
import sqlalchemy.dialects.postgresql as sapgsql


class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False)
    produkty_id = db.Column(db.ForeignKey('produkty.produkty_id'), nullable=False)
    amount = db.Column(db.Integer)
    produkt_name = db.Column(db.ForeignKey('produkty.produkt_name'))
    delivery = db.Column(db.String)
    payment_method = db.Column(db.String)
    status = db.Column(db.String)
    delivery_addres = db.Column(db.String)
    total_price = db.Column(sapgsql.MONEY)

    produkty = db.relationship('Produkty', primaryjoin='Order.produkt_name == Produkty.produkt_name', backref='produkty_orders')
    produkty1 = db.relationship('Produkty', primaryjoin='Order.produkty_id == Produkty.produkty_id', backref='produkty_orders_0')
    user = db.relationship('User', primaryjoin='Order.user_id == User.user_id', backref='orders')


class Produkty(db.Model):
    __tablename__ = 'produkty'

    produkty_id = db.Column(db.Integer, primary_key=True)
    produkt_name = db.Column(db.String, unique=True)
    value = db.Column(sapgsql.MONEY, nullable=False)
    amount = db.Column(db.Integer)
    description = db.Column(db.Text)
    typ = db.Column(db.String)
    img = db.Column(sapgsql.BYTEA)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String)
    user_id = db.Column(db.Uuid, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    surename = db.Column(db.String)
    phone = db.Column(db.Numeric)
    address = db.Column(db.String)
    postal_code = db.Column(db.Numeric)
    city = db.Column(db.String)


class Cart(db.Model):
    __tablename__ = 'cart'




