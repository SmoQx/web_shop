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

# TODO: create a db table which will contain users cart and somthing to keep track of a user cart
# TODO: add field with image to a db 

@app.route('/adduser', methods = ['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        if not (username and password and email):
            print("Missing requierd fields in user")
            return jsonify({"error": "Missing required fields"}), 400
        hashed_password = gen_password_hash(password)
        hashed_username = gen_username_hash(username)
    except Exception as e:
        print(e)
        return jsonify({"error": "No JSON data provided"}), 400

    data = request.json

    try:
        new_user = apps_db.User()
        new_user.user_id = uuid.uuid4()
        new_user.email = email
        new_user.password = hashed_password
        new_user.username = hashed_username
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
    return jsonify({"success": f"user added {username}"}), 200


@app.route('/add_item', methods = ['POST'])
def add_item():
    # TODO: check if the integer isnt to high
    int_size = 40000
    try:
        data = request.get_json()
        produkty_id = data.get("produkty_id")
        produkt_name = data.get("produkt_name")
        value = data.get("value")
        amount = data.get("amount")
        typ = data.get("typ")
        if not (produkty_id and produkt_name and value and amount and typ):
            print("Missing requierd filds in item")
            return jsonify({"error": "Missing required fields"}), 400
        if produkty_id > int_size:
            print("ID integer to high")
            return jsonify({"Error": "ID value to high"}), 408
    except Exception as e:
        print(e)
        return jsonify({"error": "error reading json"}), 408

    try:
        new_item = apps_db.Produkty()
        new_item.produkty_id = produkty_id
        new_item.produkt_name = produkt_name
        new_item.value = value
        new_item.amount = amount
        new_item.typ = typ
        db.session.add(new_item)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"error": f"an exception has occured {e}"}), 408
    print(f"Added item correctly {new_item.produkt_name} with id {new_item.produkty_id}")
    return jsonify({"success": f"added {new_item.produkt_name}"})


@app.route('/find_item', methods = ['GET'])
def find_item():
    try:
        data = request.get_json()
        item_id = data.get("item_id")
        if not (item_id):
            print("No item id")
            return jsonify({"error": "No item id"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": f"{e}"}), 400

    item_table = apps_db.Produkty

    try:
        query_for_item = db.session.query(item_table).filter_by(produkty_id = item_id).one()
        print(f"Success found item {query_for_item.produkt_name} with id {query_for_item.produkty_id}")
        return jsonify({"success": {'produkty_id': query_for_item.produkty_id, 'value': query_for_item.value, 'produkty_name': query_for_item.produkt_name}}), 200
    except Exception as e:
        print(f"Error processing querry {e}")
        return jsonify({"error": f"Error processing querry \n {e}"}), 408
    finally:
        db.session.close()


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        if not (username and password and email):
            print("Error no missing fields")
            return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "No JSON data provided"}), 400

    data = request.json
    user_table = apps_db.User

    try:
        querry_user = db.session.query(user_table).filter_by(username = gen_username_hash(username)).one()
        if querry_user.username == gen_username_hash(username) and querry_user.password == gen_password_hash(password):
            print("User authenticated")
            return jsonify({"succes": "User authenticated"}), 200
        else:
            return jsonify({"fail": "User not authentiucated"}), 203
    except Exception as e:
        print(f"Error has occured {e}")
        return jsonify({"error": f"{e}"}), 408
    finally:
        db.session.close()


@app.route('/change_item', methods = ['PUT'])
def change_item():
    try:
        data = request.get_json()
        item_id = data.get("item_id")
        what_to_change = data.get("what_to_change")
        if not type(what_to_change) == dict:
            return jsonify({"Error": "The data of what to change needs to be dictioary"}), 408
    except Exception as e:
        print(e)
        return jsonify({"Error": f"Error while processing data {e}"}), 408

    try:
        querry_produkty = db.session.get(apps_db.Produkty, item_id)
        for key, value in what_to_change.items():
            if key in vars(querry_produkty):
                setattr(querry_produkty, key, value)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"Error": f"Error while searching \n{e}"}), 408
    finally:
        db.session.close()

    return jsonify({"success": "The data was correct"}), 200


@app.route('/find_items_category', methods = ['GET'])
def find_items_category():
    try:
        data = request.get_json()
        category = data.get("category")
        if not (category):
            return jsonify({"error": "Not category"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": f"{e}"}), 400

    try:
        querry_produkty = db.session.query(apps_db.Produkty).filter_by(typ = category).all()
        temp = [x.__dict__ for x in querry_produkty]
        items_to_return = []
        for prod in temp:
            produkt = {}
            for key, item in prod.items():
                if key == '_sa_instance_state':
                    continue
                else:
                    produkt[key] = item
            items_to_return.append(produkt)
        if not querry_produkty:
            return jsonify({"Success": "Found nothing"}), 201
    except Exception as e:
        print(e)
        return jsonify({"Error": f"Error while searching \n{e}"}), 408
    finally:
        db.session.close()

    return jsonify({"Success": items_to_return}), 200


@app.route('/whats_in_the_cart')
def whats_in_cart():
    # TODO: function which will return whats in the cart based on session id or user id
    return jsonify({"success": "message"}), 200


@app.route('/add_to_cart')
def add_to_cart():
    # TODO: function which will append items to a cart based on the session or user id
    return jsonify({"success": "message"}), 200


@app.route('/remove_from_cart')
def remove_from_cart():
    # TODO: function for removeing items from cart or based on the time elapsed clear items from all carts
    return jsonify({"success": "message"}), 200


@app.route('/show_all_items')
def show_all_data():
    try:
        data = request.get_json()
        print(data)
        message = data.get('message')
        if 'show' in message:
            query_items = db.session.query(apps_db.Produkty).all()
        else:
            return jsonify({'error': 'wrong command to show data'}), 400
    except Exception as e:
        return jsonify({'error': e}), 400
    return jsonify({'success': query_items}), 200


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


if __name__ == '__main__':
    app.run(debug=True, host='::', port=80)

