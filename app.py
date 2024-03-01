from flask import Flask, render_template, request, redirect, url_for, send_file, after_this_request
from flask_sqlalchemy import SQLAlchemy
#from app_db import db, users


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:app@localhost/app'
db = SQLAlchemy(app)
#user_db = users(db.Model)
class TeamData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(200))
    team2 = db.Column(db.String(200))

@app.route('/adduser/<name>')
def add_user(name):
    db.session.add(user_db(name=name, surename=name))
    db.session.commit()
    return f"added {name}"


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
