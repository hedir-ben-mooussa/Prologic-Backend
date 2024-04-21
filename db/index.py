import datetime
from enum import Enum
from flask import app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_utils import database_exists, create_database


db = SQLAlchemy()

class SensorType(Enum):
     TEMPERATURE = 'Temperature'
     HUMIDITY = 'Humidity'
     GAS = 'Gas'
 

class Sensors(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     date = db.Column(db.Date, nullable=False)
     value = db.Column(db.Float, nullable=False)
     maxValue = db.Column(db.Float, nullable=False)
     sensortype = db.Column(db.Enum(SensorType), nullable=False)


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/Prologic_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            print("Database created.")
        db.create_all()
        print("Tables created.")
    return db 