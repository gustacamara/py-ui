#include <ESP32Servo.h>
#include <WiFi.h> 
#include "PubSubClient.h"
#include <ArduinoJson.h>
#include "ServoEasing.hpp"
#include <SPI.h>
#include <MFRC522.h>

#define WIFI_SSID ""
#define WIFI_PASSWORD ""

#define MQTT_TOPIC "pyui/accessories-9P5nN15kdp"
#define MQTT_SERVER "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_CLIENT_ID "pyui-accessories-MhiEKhUQWv"

#define IR_SENSOR_PIN 2
#define SERVO_PIN 5

#define RFID_SS_PIN 21
#define RFID_RST_PIN 22

MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);

ServoEasing servo;
int previousIrSensorState = -1;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void handleServo(int value) {
  servo.easeTo(value, 45);
}

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
    handleServo(doc["value"]);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.flush();

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
  mqttClient.setCallback(mqttMessageCallback);

  // Setup IR
  pinMode(IR_SENSOR_PIN, INPUT);

  // Setup Servo
  servo.attach(SERVO_PIN);
  servo.write(0);

  // Setup RFIR
  SPI.begin();
  rfid.PCD_Init();
}

void connectMqtt() {
  while (!mqttClient.connected()) {
    Serial.print("[mqtt] Connecting...");
    if (mqttClient.connect(MQTT_CLIENT_ID)) {
      Serial.print("[mqtt] Connected...");
      mqttClient.subscribe(MQTT_TOPIC);
    }
    else {
      Serial.print(".");
      delay(1000);
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
