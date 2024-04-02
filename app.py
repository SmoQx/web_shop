from flask import Flask, render_template, request, redirect, url_for, send_file, after_this_request
from flask_sqlalchemy import SQLAlchemy
import apps_db
import uuid
from gen_password import gen_password_hash
from gen_username_hash import gen_username_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@127.0.0.1:40266/app'
db = SQLAlchemy(app=app)


@app.route('/adduser/<name>')
def add_user(name):
    
    new_user = apps_db.User(
            user_id = uuid.uuid4(),
            email = f"{name}@mail.com",
            password = gen_password_hash(name),
            username = gen_username_hash(name),
            name = name
            )
    db.session.add(new_user)
    db.session.commit()
    return f"added {name}"


@app.route('/additem/<item>')
def add_item(item: str) -> str:
    new_item = apps_db.Produkty(produkty_id = 5,
                                produkt_name = item,
                                value = "10,00",
                                amount = "0",
                                typ = "figurine"
                                )

    db.session.add(new_item)
    db.session.commit()

    return f"added {item}"

@app.route('/')
def main():
    # TODO: REDNER ALL ITEMS LIST
    return render_template('index.html')


@app.route('/about')
def about():
    # TODO: Redirect to contact page
    return render_template('about.html')


@app.route('/contact')
def contact():
    # TODO: form to contact
    return render_template('contact.html')


@app.route('/item/<item_id>')
def display_item(item_id):
    print("ITEM ID IS ", item_id)
    # TODO: get an item from db
    return render_template('item.html')


@app.route('/user/<user_id>')
def user_page(user_id):
    print("USER ID IS", user_id)
    # TODO: User page
    return render_template('user.html')


@app.route('/yes')
def yes():
    print("yessss")
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True, host='::', port=80)
