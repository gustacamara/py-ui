#include <ESP32Servo.h>
#include <WiFi.h>
#include "PubSubClient.h"
#include <ArduinoJson.h>
#include <ESP32Servo.h>
#include <SPI.h>
#include <MFRC522.h>

#define WIFI_SSID ""
#define WIFI_PASSWORD ""

#define MQTT_TOPIC "pyui/accessories-9P5nN15kdp"
#define MQTT_SERVER "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_CLIENT_ID "pyui-accessories-MhiEK"

#define IR_SENSOR_PIN 2
#define SERVO_1_PIN 5
#define SERVO_2_PIN 15

#define RFID_SS_PIN 21
#define RFID_RST_PIN 22

MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);

Servo servo1;
Servo servo2;
int previousIrSensorState = -1;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void mqttMessageCallback(char* topic, byte* rawPayload, unsigned int length) {
  Serial.print("[mqtt] Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  String payload = "";
  for (int i = 0; i < length; i++) {
    payload += (char)rawPayload[i];
  }
  Serial.print(payload);
  Serial.print("\n");

  JsonDocument doc;
  deserializeJson(doc, payload);

  if (doc["actuator"] == "SERVO" && doc["id"] == 1) {
    int val = doc["value"];
    servo1.write(val);
  }

  if (doc["actuator"] == "SERVO" && doc["id"] == 2) {
    int val = doc["value"];
    servo2.write(val);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.flush();

  // Setup IR
  pinMode(IR_SENSOR_PIN, OUTPUT);

  // Setup Servo
  servo1.attach(SERVO_1_PIN);
  servo2.attach(SERVO_2_PIN);
  servo1.write(0);
  servo2.write(60);

  // Setup Wifi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("[wifi] Connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.print("\n");
  Serial.print("[wifi] Connected\n");

  // Setup MQTT Client
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setSocketTimeout(30);
  mqttClient.setCallback(mqttMessageCallback);

  // Setup RFIR
  SPI.begin();
  rfid.PCD_Init();
}

void connectMqtt() {
  while (!mqttClient.connected()) {
    Serial.print("[mqtt] Connecting...\n");

    pinMode(IR_SENSOR_PIN, OUTPUT);
    digitalWrite(IR_SENSOR_PIN, LOW);
    delay(150);
    digitalWrite(IR_SENSOR_PIN, HIGH);
    delay(150);
    digitalWrite(IR_SENSOR_PIN, LOW);
    delay(150);
    digitalWrite(IR_SENSOR_PIN, HIGH);

    if (mqttClient.connect(MQTT_CLIENT_ID)) {
      Serial.print("[mqtt] Connected...\n");
      mqttClient.subscribe(MQTT_TOPIC);
      pinMode(IR_SENSOR_PIN, INPUT_PULLUP);
    }
    else {
      Serial.printf("Error: %d\n", mqttClient.state());
    }
  }
}

void handleIRSensor() {
  int irSensorState = digitalRead(IR_SENSOR_PIN);

  if (irSensorState == previousIrSensorState) {
    return;
  }

  previousIrSensorState = irSensorState;

  JsonDocument doc;
  doc["id"] = 2;
  doc["sensor"] = "IR";
  doc["value"] = irSensorState == LOW;

  String message;
  serializeJson(doc, message);
  mqttClient.publish(MQTT_TOPIC, message.c_str());
}

void handleRFIDSensor() {
  if (!rfid.PICC_IsNewCardPresent())
    return;

  if (!rfid.PICC_ReadCardSerial())
    return;

  MFRC522::StatusCode status;
  byte buffer[18];
  byte size = sizeof(buffer);

  status = (MFRC522::StatusCode) rfid.MIFARE_Read(0x06, buffer, &size);
  if (status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Read() failed: "));
    Serial.println(MFRC522::GetStatusCodeName(status));
    return;
  }

  uint32_t cabId = (buffer[0] << 24) + (buffer[1] << 16) + (buffer[2] << 8) + buffer[3];
  Serial.printf("Read cabId %d\n", cabId);
  rfid.PICC_HaltA();

  JsonDocument doc;
  doc["id"] = 1;
  doc["sensor"] = "RFID";
  doc["value"] = cabId;

  String message;
  serializeJson(doc, message);
  mqttClient.publish(MQTT_TOPIC, message.c_str());
}

void loop() {
  connectMqtt();
  mqttClient.loop();
  handleIRSensor();
  handleRFIDSensor();
}
