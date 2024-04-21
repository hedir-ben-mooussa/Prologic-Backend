import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import Migrate

db = SQLAlchemy()

#enum

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    temperature_value = db.Column(db.Float, nullable=False)
    humidity_value = db.Column(db.Float, nullable=False)
    Gas_value = db.Column(db.Float, nullable=False)

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/statDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # migrate = Migrate(app, db)

    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            print("Database created.")
        db.create_all()
        print("Tables created.")
