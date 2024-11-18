from flask_mqtt import Mqtt #pip install flask-mqtt
import json
from lib.dccpp import generateDccThrottleCmd, generateDccFunctionCmd
from flask import Blueprint, request, render_template
client = Blueprint("client",__name__, template_folder="templates")

sensors_values = {
    1: {
        "id": 0,
        "location": "Restaurante 8bits",
        "type": "RFID",
        "value": 0
    },
    2: {
        "id": 1,
        "location": "Parada das capivaras",
        "type": 'Infravermelho',
        "value": 'false'
    }
}

turnouts = {
    1: {
        "id": 1,
        "left": 0,
        "right": 60
    },
    2: {
        "id": 2,
        "left": 0,
        "right": 60
    }
}

mqtt_client = Mqtt()

def init_mqtt(app):
    global mqtt_client

    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False

    mqtt_client.init_app(app)

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

    if data["path"] == "inner":
      servo1Angle = 60
      servo2Angle = 0
    else:
      servo1Angle = 0
      servo2Angle = 60

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
    global turnouts

    return render_template("real_time.html", sensors_values = sensors_values, actuator_values = turnouts)

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

    try:
        print(message.payload.decode())
        data = json.loads(message.payload.decode())
        if "sensor" in data:
            sensors_values[data["id"]] = data

        if "actuator" in data:
            turnouts[data["id"]] = data

    except:
        pass

