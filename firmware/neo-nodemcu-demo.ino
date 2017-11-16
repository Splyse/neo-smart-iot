#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <Adafruit_NeoPixel.h>
#include <PubSubClient.h>
#include <Wire.h>

/* 
Neo Smart IoT demo sketch for NodeMCU device
(c) 2017 Splyse Inc.

MIT License

This sketch should be connected to a NeoPixels strip
with pin D1 connected to the data port of the strip
*/


const char* ssid = "Your_Network_SSID";
const char* password = "Your_WiFi_password";
const char* mqtt_server = "ip_or_hostname_of_neo-pubsub_node";

WiFiClient espClient;
PubSubClient client(espClient);

#define LED D0
#define PIN D1
#define BRIGHTNESS 50

bool ledState;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(10, PIN, NEO_GRB + NEO_KHZ800);

void lightstrip(uint32_t color)
{
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
  }
    strip.show();
}

void callback(char* topic, byte* payload, unsigned int length) {
 Serial.print("Message arrived [");
 Serial.print(topic);
 Serial.print("] ");
 uint32_t requestedcolor = 0;

 if (length != 3)
 {
   Serial.println("Received invalid RGB value");
   return;
 }
 requestedcolor = payload[2] | (payload[1] << 8) | (payload[0] << 16);
 lightstrip(requestedcolor);
}


void reconnect() {
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 if (client.connect("ESP8266 Client")) {
  lightstrip(0x00ff00);
  Serial.println("connected");
  client.subscribe("Neo/b3a14d99a3fb6646c78bf2f4e2f25a7964d2956a/test");
 } else {
  lightstrip(0x00ffff);
  Serial.print("failed, rc=");
  Serial.print(client.state());
  Serial.println(" try again in 5 seconds");
  delay(5000);
  }
 }
}

void setup()
{
 strip.begin();
 strip.setBrightness(BRIGHTNESS);

 lightstrip(0xff0000);

 Serial.begin(9600);

 Serial.print("Connecting to ");
 Serial.println(ssid);

 WiFi.begin(ssid, password);

 while (WiFi.status() != WL_CONNECTED) {
   delay(500);
 }
 Serial.print("WiFi connected, local ip is ");
 Serial.println(WiFi.localIP());

 lightstrip(0x00ffff);

 client.setServer(mqtt_server, 1883);
 client.setCallback(callback);
 pinMode(LED, OUTPUT);
}

void loop()
{
 delay(500);
 digitalWrite(LED, ledState);
 ledState = !ledState;
 if (!client.connected()) {
  reconnect();
 }
 client.loop();
}
