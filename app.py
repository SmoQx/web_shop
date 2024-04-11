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
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not (username and password and email):
            return jsonify({"error": "Missing required fields"}), 400
        hashed_password = gen_password_hash(password)
        hashed_username = gen_username_hash(username)
    except Exception as e:
        print(e)
        return jsonify({"error": "No JSON data provided"}), 400
    data = request.json
    try:
        new_user = apps_db.User(
                                user_id = uuid.uuid4(),
                                email = email,
                                password = hashed_password,
                                username = hashed_username,
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
    print(f"User succesfouly added {username}")
    return jsonify({"success": f"user added {username}"}), 201


@app.route('/additem')
def add_item(item: str):
    try:
        data = request.get_json()
        produkty_id = data.get("produkty_id")
        produkt_name = data.get("produkt_name")
        value = data.get("value")
        amount = data.get("amount")
        typ = data.get("typ")

        if not (produkty_id and produkt_name and value and amount and typ):
            return jsonify({"error": "Missing required fields"}), 400

    except Exception as e:
        print(e)
        return jsonify({"error": "error reading json"}), 408
    if "produkty_id" in data and "produkt_name" in data and "value" in data and "typ" in data:
        try:
            new_item = apps_db.Produkty(
                                        produkty_id = produkty_id,
                                        produkt_name = produkt_name,
                                        value = value,
                                        amount = amount,
                                        typ = typ
                                        )

            db.session.add(new_item)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"error": f"an exception has occured {e}"}), 408
        finally:
            db.session.close()
    return f"added {item}"


@app.route('/find_item/<item_id>', methods = ['GET', 'POST'])
def find_item(item_id):
    item_id = item_id
    item_table = apps_db.Produkty
    try:
        query_for_item = db.session.query(item_table).filter_by(produkty_id = item_id).one()
        return jsonify({"success": f"retured {query_for_item.produkty_id, query_for_item.value, query_for_item.produkt_name}"}), 201
    except Exception as e:
        return jsonify({"error": f"Error processing querry \n {e}"}), 408
    finally:
        db.session.close()


@app.route('/login/<username>,<password>')
def login(username: str, password: str):
    user_table = apps_db.User
    try:
        querry_user = db.session.query(user_table).filter_by(username = gen_username_hash(username)).one()
        if querry_user.username == gen_username_hash(username) and querry_user.password == gen_password_hash(password):
            return jsonify({"succes": "User authenticated"}), 201
        else:
            return jsonify({"fail": "User not authentiucated"}), 203
    except Exception as e:
        return jsonify({"error": f"{e}"}), 408
    finally:
        db.session.close()


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
