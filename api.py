from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
from db.index import SensorType, Sensors, init_app


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db=init_app(app)


@app.route('/',methods=["GET"])
def hello():
    name = request.args.get("name", "world")
    return 'Hello'

# Create a sensor
@app.route('/sensor', methods=['POST'])
def create_sensor():
    data = request.get_json()
    new_sensor = Sensors(date=datetime.now(),
                         value=data['value'],
                         maxValue=data['maxValue'],
                         sensortype=SensorType[data['sensortype']])
    print("zz",new_sensor)
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor created successfully'}), 201

# Read all sensors
@app.route('/sensor', methods=['GET'])
def get_sensors():
    sensors = Sensors.query.all()
    result = []
    for sensor in sensors:
        result.append({'id': sensor.id,
                       'date': sensor.date,
                       'value': sensor.value,
                       'maxValue': sensor.maxValue,
                       'sensortype': sensor.sensortype.value})
    return jsonify(result)

# Update a sensor
@app.route('/sensor/<int:sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    sensor = Sensors.query.get(sensor_id)
    if sensor:
        data = request.get_json()
        sensor.date = data['date']
        sensor.value = data['value']
        sensor.maxValue = data['maxValue']
        sensor.sensortype = SensorType[data['sensortype']]
        db.session.commit()
        return jsonify({'message': 'Sensor updated successfully'})
    else:
        return jsonify({'message': 'Sensor not found'}), 404

# Delete a sensor
@app.route('/sensor/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    sensor = Sensors.query.get(sensor_id)
    if sensor:
        db.session.delete(sensor)
        db.session.commit()
        return jsonify({'message': 'Sensor deleted successfully'})
    else:
        return jsonify({'message': 'Sensor not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
