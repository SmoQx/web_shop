from flask import Flask, Request, render_template, request, redirect, url_for, send_file, after_this_request, jsonify 
from werkzeug.wrappers import response
from flask_sqlalchemy import SQLAlchemy
import json
import apps_db
import uuid
from gen_password import gen_password_hash
from gen_username_hash import gen_username_hash


app = Flask(__name__)

with open("login.json", 'r') as read_login:
    read_data =json.load(read_login)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{read_data["user"]}:{read_data["password"]}@{read_data["address"]}:{read_data["port"]}/{read_data["db"]}'

db = SQLAlchemy(app=app)


# TODO: create user reader 
# TODO: create a item adder 
# TODO: add field with image to a db 
# TODO: create function to return items based on category

@app.route('/adduser', methods = ['POST'])
def add_user():
    # TODO: write a checker for the data
    try:
        request.get_json()
    except Exception as e:
        return e
    data = request.json
    if "name" in data:
        name = data["name"]
        new_user = apps_db.User(
                                user_id = uuid.uuid4(),
                                email = f"{data['email']}",
                                password = gen_password_hash(data['password']),
                                username = gen_username_hash(data['username']),
                                name = data['name']
                                )
        db.session.add(new_user)
        db.session.commit()
        return f"added {name}"
    else:
        return f"Failed to parse json"


@app.route('/additem/<item>')
def add_item(item: str) -> str:
    new_item = apps_db.Produkty(produkty_id = 9,
                                produkt_name = item,
                                value = "10,00",
                                amount = "0",
                                typ = "figurine"
                                )

    db.session.add(new_item)
    db.session.commit()

    return f"added {item}"


@app.route('/json', methods = ['POST'])
def data_parser():
    content = request.get_json()
    content = dict(content)
    for key, value in content.items():
        print(f"key = {key}: value = {value}")
    repsonse_data = {
        "status": "success",
        "data": content
            }
    return jsonify(repsonse_data), 200
    

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


if __name__ == '__main__':
    app.run(debug=True, host='::', port=80)
