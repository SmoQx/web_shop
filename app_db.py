from flask import Flask, render_template, request, redirect, url_for, send_file, after_this_request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app=app)
#user_db = users(db.Model)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    value = db.Column(db.String(200))
    amount = db.Column(db.String(200))
    typ = db.Column(db.String(200))
    description = db.Column(db.String(500))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    name = db.Column(db.String(200))
    surename = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    addres = db.Column(db.String(200))
    postal_code = db.Column(db.String(200))
    city = db.Column(db.String(200))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)



#with app.app_context():
#    db.create_all()

#def db(app):
#    
#    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:app@localhost/app'
#    db = SQLAlchemy(app)
#
#    return db


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=80)
