from flask_sqlalchemy import SQLAlchemy


def db(app):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:app@localhost/app'
    db = SQLAlchemy(app)

    return db


if __name__ == "__main__":
    pass
