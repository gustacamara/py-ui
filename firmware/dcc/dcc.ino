#include <ESP8266WiFi.h>
#include "PubSubClient.h"

#define WIFI_SSID ""
#define WIFI_PASSWORD ""

#define MQTT_TOPIC "pyui/dcc-K3xWvP4p4D"
#define MQTT_SERVER "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_CLIENT_ID "pyui-dcc-A3Bbbclslk"

// #define ENABLE_DEBUG true

#ifdef ENABLE_DEBUG
#define DEBUG_PRINT(...) Serial.printf(__VA_ARGS__)
#else
#define DEBUG_PRINT(...)
#endif

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void mqttMessageCallback(char* topic, byte* rawPayload, unsigned int length) {
  DEBUG_PRINT("[mqtt] Message arrived [");
  DEBUG_PRINT(topic);
  DEBUG_PRINT("] ");

  String payload = "";
  for (int i = 0; i < length; i++) {
    payload += (char)rawPayload[i];
  }
  Serial.print(payload);
  DEBUG_PRINT("\n");
}

void setup() {
  Serial.begin(115200);
  Serial.flush();
  Serial.print("<t 1 3 0 0>");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  DEBUG_PRINT("[wifi] Connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    DEBUG_PRINT(".");
  }
  DEBUG_PRINT("\n");
  DEBUG_PRINT("[wifi] Connected\n");

  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setSocketTimeout(30);
  mqttClient.setCallback(mqttMessageCallback);
}

void connectMqtt() {
  while (!mqttClient.connected()) {
    Serial.print("<f 3 128>");
    delay(250);
    Serial.print("<f 3 145>");
    delay(250);
    Serial.print("<f 3 128>");
    delay(250);
    Serial.print("<f 3 145>");

    DEBUG_PRINT("[mqtt] Connecting...\n");
    if (mqttClient.connect(MQTT_CLIENT_ID)) {
      DEBUG_PRINT("[mqtt] Connected...\n");
      Serial.print("<f 3 128>");
      mqttClient.subscribe(MQTT_TOPIC);
    }
    else {
      DEBUG_PRINT("Error: %d\n", mqttClient.state());
    }
  }
}

void loop() {
  connectMqtt();
  mqttClient.loop();
}
