from flask_mqtt import Mqtt #pip install flask-mqtt
import json
from lib.dccpp import generateDccThrottleCmd, generateDccFunctionCmd
from flask import Blueprint, request, render_template, redirect, url_for, current_app
client = Blueprint("client",__name__, template_folder="templates")

sensors_values = {
    1: {
        "id": 1,
        "sensor": "RFID",
        "value": "3560"
    },
    2: {
        "id": 2,
        "sensor": "IR",
        "value": True
    }
}

turnouts = [
    {
        "id": 1,
        "actuator": "SERVO",
        "value": 128
    },
    {
        "id": 2,
        "actuator": "SERVO",
        "value": 128
    }
]

mqtt_client = Mqtt()

@client.before_app_request
def init_mqtt():
    global mqtt_client
    if not mqtt_client._connect_handler:
        # Set MQTT config within the application context
        current_app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
        current_app.config['MQTT_BROKER_PORT'] = 1883
        current_app.config['MQTT_USERNAME'] = '' 
        current_app.config['MQTT_PASSWORD'] = '' 
        current_app.config['MQTT_KEEPALIVE'] = 5000 
        current_app.config['MQTT_TLS_ENABLED'] = False
        
        mqtt_client.init_app(current_app)

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

    turnoutValue = 0 if data["direction"] == "left" else 128 # Ajust angles 

    cmd = {
        "id": data["id"],
        "actuator": "SERVO",
        "value": turnoutValue
    }

    publish_to_mqtt(topic_accessories , json.dumps(cmd))
    return ""

@client.route('/get_sensors_values', methods=['GET'])
def get_sensors_values():
    global sensors_values

    return render_template("real_time.html", sensors_values = sensors_values)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_accessories)
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global sensors_values

    data = json.loads(message.payload.decode())
    print(str(data))
    
    if "sensor" in data:
        sensors_values[data["id"]] = data
        print(sensors_values)
