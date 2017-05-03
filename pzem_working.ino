#include <SoftwareSerial.h>
#include <PZEM004T.h>
#include <ESP8266WiFi.h>

const char* ssid = "x1";
const char* password = "pass";

PZEM004T pzem(4,5);  // RX,TX (D2, D1) on NodeMCU
IPAddress ip(192,168,1,1);

WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  pzem.setAddress(ip);
  
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  Serial.println(WiFi.localIP());

 // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());

}

void loop() {
 // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
      
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  //String req = client.readStringUntil('\r');
 // Serial.println(req);
 // client.flush();
  
  
  float v = pzem.voltage(ip);
  wdt_reset();
  Serial.print(v);Serial.print("V; ");

  float i = pzem.current(ip);
  wdt_reset();
  Serial.print(i);Serial.print("A; ");
  
  float p = pzem.power(ip);
  wdt_reset();
  Serial.print(p);Serial.print("W; ");
  
  float e = pzem.energy(ip);
  wdt_reset();
  Serial.print(e);Serial.print("Wh; ");

  String payload = "meter voltage=" + String(v, 2);
  payload += ",current=" + String(i, 2);
  payload += ",power=" + String(p, 2);
  payload += ",energy=" + String(e, 2);
   // Prepare the response
  
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\n ";
  s += payload;
  s += "</html>\n";

  // Send the response to the client
  client.print(s);
  
  Serial.println();

  delay(5000);
}