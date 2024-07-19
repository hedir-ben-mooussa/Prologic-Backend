import eventlet
# from services.video import SimpleFacerec
eventlet.monkey_patch()
import json, os
import face_recognition
from datetime import datetime
from services.database import MySQLSingleton
from flask import Flask, jsonify, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from services.facial_recognition import recognize_face_service
from werkzeug.utils import secure_filename
import cv2



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "faces"
app.config['TEMP_FOLDER'] = "temp"
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.app_context()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '172.19.14.118'
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
    mqtt.subscribe('datacenter/auth')
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
    name = request.form["name"]
    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    mysqlClient.add_face(name, filename)
    return jsonify({'message': 'Image saved successfully'})

@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['TEMP_FOLDER'], filename))
    unknown_image = face_recognition.load_image_file(os.path.join(app.config['TEMP_FOLDER'], filename))
    try:
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    except:
        return jsonify({"status":False, "reason": "Cannot detect a human face."})
    faces = mysqlClient.get_saved_users()
    encodings = []
    for face in faces:
        known_image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_FOLDER'], face["picture"]))
        known_encoding = face_recognition.face_encodings(known_image)[0]
        encodings.append(known_encoding)
    results = face_recognition.compare_faces(encodings, unknown_encoding)
    for resultIndex in range(len(results)):
        if results[resultIndex]:
            faces[resultIndex]["status"] = True
            return jsonify(faces[resultIndex])
    return jsonify({"status":False, "reason": "User not signed up"})

# sfr = SimpleFacerec()
# sfr.load_encoding_images("faces/")
# @app.route('/recognize_face', methods=['POST'])
# def run_python_code():

#     cap = cv2.VideoCapture(0)
#     recognized = False
#     nbusers = 0

#     while True:
#         ret, frame = cap.read()

#         face_locations, face_names = sfr.detect_known_faces(frame)
#         for face_loc, name in zip(face_locations, face_names):
#             if name != "Unknown" and not recognized:
#                 print("Recognized:", name)
#                 recognized = True
#                 nbusers += 1
#                 print("nbusers:", nbusers)

#         cv2.imshow("Frame", frame)
#         if cv2.waitKey(1) & 0xFF == ord('s'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return jsonify({
#        "nbusers:" : nbusers ,
#        "isrecognise" : recognized
#   })




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
