import eventlet
eventlet.monkey_patch()
import json
from datetime import datetime
from services.database import MySQLSingleton
from flask import Flask, jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from services.facial_recognition import recognize_face_service, uploadService

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.app_context()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.1.23'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

mysqlClient = MySQLSingleton(user='root', password='',host='127.0.0.1',port="3306", database='prologic_db')



@app.route('/getTemperature', methods=["GET"])
def getTemperature():
    temperature_values = mysqlClient.get_temperature_values()
    return jsonify({'temperature_values': temperature_values})

@app.route('/getGas', methods=["GET"])
def getGas():
    gas_values = mysqlClient.get_gas_values()
    return jsonify({'gas_values': gas_values})

@app.route('/getHumidity', methods=["GET"])
def getHumidity():
    humidity_values = mysqlClient.get_humidity_values()
    return jsonify({'humidity_values': humidity_values})


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('datacenter/temperature')
    mqtt.subscribe('datacenter/humidity')
    mqtt.subscribe('datacenter/gas')
    mqtt.subscribe('datacenter/flame')
    print('MQTT Connected')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        value=message.payload.decode()
    )
    date = datetime.now()
    
    match data["topic"]:
        case 'datacenter/temperature':
            print(data['value'])
            mysqlClient.insert_temperature(value=data['value'], date=date)
        case 'datacenter/humidity':
            print(data['value'])
            mysqlClient.insert_humidity(value=data['value'], date=date)
        case 'datacenter/gas':
            print(data['value'])
            mysqlClient.insert_gas(value=data['value'], date=date)
    
@app.route('/upload', methods=['POST'])
def upload():
    return uploadService()

@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    return recognize_face_service()

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=False, debug=True)