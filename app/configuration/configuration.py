from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DATABASE_URI = 'sqlite:///app.db'

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)