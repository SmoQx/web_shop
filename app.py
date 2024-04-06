from flask import Flask, Request, render_template, request, redirect, url_for, send_file, after_this_request, jsonify 
from werkzeug.wrappers import response
from flask_sqlalchemy import SQLAlchemy
import json
import apps_db
import uuid
from gen_password import gen_password_hash
from gen_username_hash import gen_username_hash
import sqlalchemy.exc


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
    try:
        request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not (username and password and email):
            return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "error reading json"}), 408
    data = request.json
    if "username" in data and "password" in data and "email" in data:
        try:
            new_user = apps_db.User(
                                    user_id = uuid.uuid4(),
                                    email = f"{data['email']}",
                                    password = gen_password_hash(data['password']),
                                    username = gen_username_hash(data['username']),
                                    )
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as already_in:
            print(already_in)
            return jsonify({"error": "user already exists"}), 409
        except Exception as e:
            print(e)
            return jsonify({"error": "an error has ccured"}), 408
        finally:
            db.session.close()
        print(f"User succesfouly added {data['username']}")
        return jsonify({"success": f"user added {data['username']}"}), 201
    else:
        return jsonify({"error": "failed to parse json wrong data"}), 408


@app.route('/additem')
def add_item(item: str):
    try:
        request.get_json()
    except Exception as e:
        print(e)
        return jsonify({"error": "error reading json"}), 408
    data = request.json
    if "produkty_id" in data and "produkt_name" in data and "value" in data and "typ" in data:
        try:
            new_item = apps_db.Produkty(
                                        produkty_id = data["produkty_id"],
                                        produkt_name = data["produkt_name"],
                                        value = data["value"],
                                        amount = data["amount"],
                                        typ = data["typ"]
                                        )

            db.session.add(new_item)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"error": f"an exception hs occured {e}"}), 408
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
    

def search():
    pass


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
