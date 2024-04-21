from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)
mqtt = Flask (__name__)

app.config['MQTT_BROKER_URL'] = 'mosquitto broker url'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

@app.route("/")


def home() : 
    return "Hello from flask"

# subscribe to a topic
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('datacenter/temperature')
    
#publish
mqtt.publish('datacenter/temperature', 'temperature')