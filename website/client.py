from flask_mqtt import Mqtt #pip install flask-mqtt
from time import localtime, strftime
from utils.db_utils import start_query
import json
from lib.dccpp import generateDccThrottleCmd, generateDccFunctionCmd
from flask import Blueprint, request, render_template
client = Blueprint("client",__name__, template_folder="templates")

sensors_values = {}
turnouts_values = {}

mqtt_client = Mqtt()

def init_mqtt(app):
    global mqtt_client

    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False

    init_realtime_values()
    mqtt_client.init_app(app)


def init_realtime_values():
    global sensors_values
    global turnouts_values

    sensors = start_query("SELECT * FROM sensor ORDER BY id")
    for sensor in sensors:
        sensors_values[sensor[0]] = { "value": 0, "time": "" }

    turnouts = start_query("SELECT * FROM turnout ORDER BY id")
    for turnout in turnouts:
        turnouts_values[turnout[0]]= { "value": 0, "time": "" }

topic_dcc = "pyui/dcc-K3xWvP4p4D"
topic_accessories = "pyui/accessories-9P5nN15kdp"


# Handle MQTT
def publish_to_mqtt(topic, message):
    mqtt_client.publish(topic, message)

@client.route('/send_dcc_cmd', methods=['POST'])
def send_dcc_cmd():
    global topic_dcc

    data = request.get_json()

    cabId = data["cab"] or 3
    speed = data["speed"]
    direction = data["direction"]
    frontLight = data["frontLight"]
    secondaryLights = data["secondaryLight"]
    cmds = generateDccThrottleCmd(cabId, speed, direction)
    cmds += generateDccFunctionCmd(cabId, frontLight, secondaryLights)

    publish_to_mqtt(topic_dcc, cmds)
    return ""

@client.route('/send_turnout_cmd', methods=['POST'])
def send_turnout_cmd():
    global topic_accessories

    data = request.get_json()
    servos = start_query("SELECT * FROM turnout ORDER BY id")

    if data["path"] == "inner":
      servo1Angle = servos[0][2]
      servo2Angle = servos[1][2]
    else:
      servo1Angle = servos[0][1]
      servo2Angle = servos[1][1]

    publish_to_mqtt(topic_accessories, json.dumps({
        "id": 1,
        "actuator": "SERVO",
        "value": servo1Angle
    }))

    publish_to_mqtt(topic_accessories, json.dumps({
        "id": 2,
        "actuator": "SERVO",
        "value": servo2Angle
    }))

    return ""

@client.route('/get_sensors_values', methods=['GET'])
def get_sensors_values():
    global sensors_values
    global turnouts_values

    sensors_with_values = {}
    sensors = start_query("SELECT * FROM sensor ORDER BY id")
    for sensor in sensors:
        sensors_with_values[sensor[0]] = {
            "id": sensor[0],
            "location": sensor[1],
            "type": sensor[2],
            "value": sensors_values.get(sensor[0], {}).get("value", False),
            "time": sensors_values.get(sensor[0], {}).get("time", "")
        }

    turnouts_with_values = {}
    turnouts = start_query("SELECT * FROM turnout ORDER BY id")
    for turnout in turnouts:
        turnouts_with_values[turnout[0]] = {
            "id": turnout[0],
            "left": turnout[1],
            "right": turnout[2],
            "value": turnouts_values.get(turnout[0], {}).get("value", 0),
            "time": turnouts_values.get(turnout[0], {}).get("time", "")
        }

    return render_template("real_time.html", sensors_values = sensors_with_values, turnouts_values = turnouts_with_values)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_accessories)
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect():
    print("Disconnected from broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global sensors_values
    global turnouts_values

    try:
        data = json.loads(message.payload.decode())
        print(data)
    except:
        return

    if "sensor" in data:
        sensors_values[data["id"]] = { "value": data['value'], "time": strftime("%H:%M:%S", localtime()) }

    if "actuator" in data:
        turnouts_values[data["id"]] = { "value": data['value'], "time": strftime("%H:%M:%S", localtime()) }

    store_sensor_history(data)

def store_sensor_history(data):
    if 'sensor' in data:
        sensor_id = data['id']
        actuator_id = 'NULL'
        type = 'SENSOR'
        description = data['sensor']
    else:
        sensor_id = 'NULL'
        actuator_id = data['id']
        type = 'ATUADOR'
        description = data['actuator']

    queryStr = "INSERT INTO sensors_history(value, datetime, sensor_id, actuator_id, type, description) VALUES ('{}', '{}', {}, {}, '{}', '{}')"
    query = queryStr.format(
        str(data['value']),
        strftime("%Y-%m-%d %H:%M:%S", localtime()),
        sensor_id,
        actuator_id,
        type,
        description)

    start_query(query)
