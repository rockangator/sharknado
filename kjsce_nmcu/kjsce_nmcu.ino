
uint8_t m1 = D1; //R
uint8_t m2 = D2; //L
uint8_t m3 = D3; //F
uint8_t m4 = D4; //B

//int l1 = 2;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(m4, OUTPUT);
  //pinMode(l1,OUTPUT);
}

// the loop function runs over and over again forever
void loop() {

  analogWrite(m1, 512);
  analogWrite(m2,0);
  delay(2000);

  analogWrite(m2, 512);
  analogWrite(m1,0);
  delay(2000);

  analogWrite(m3, 512);
  analogWrite(m4,0);
  delay(2000);

  analogWrite(m4, 512);
  analogWrite(m3,0);
  delay(2000);

  digitalWrite(m1, HIGH);
  digitalWrite(m2, LOW);
  delay(1000);

  digitalWrite(m2, HIGH);
  digitalWrite(m1, LOW);
  delay(1000);
}



////const int LED_ao = 2;
////void setup()  {    
////  pinMode(LED_ao, OUTPUT); 
////}  
////void loop()  { 
////  for (int brightness=0; brightness<=1024; brightness++)  
////    {
////      analogWrite(LED_ao, brightness);  
////      delay(10);                         
////    }
////  for (int brightness=1024; brightness>=0; brightness--) 
////    {
////      analogWrite(LED_ao, brightness);  
////      delay(10);     
////    }                           
////}
//



//
//#include <ESP8266WiFi.h>
//#include <PubSubClient.h>
//
//// Update these with values suitable for your network.
//
//const char* ssid = "GREAT44";
//const char* password = "qwertyuiop";
//const char* mqtt_server = "192.168.43.217";
//
//const char* mqttUser = "username";
//const char* mqttPassword = "qwertyuiop";
//
//WiFiClient espClient;
//PubSubClient client(espClient);
//
//long lastMsg = 0;
//char msg[50];
//int value = 0;
//
//void setup() {
//  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
//  Serial.begin(115200);
//  setup_wifi();
//  client.setServer(mqtt_server, 1883);
//  client.setCallback(callback);
//}
//
//void setup_wifi() {
//
//  delay(10);
//  // We start by connecting to a WiFi network
//  Serial.println();
//  Serial.print("Connecting to ");
//  Serial.println(ssid);
//  
//  WiFi.mode(WIFI_STA);
//  WiFi.begin(ssid, password);
//
//  while (WiFi.status() != WL_CONNECTED) {
//    delay(500);
//    Serial.print(".");
//  }
//
//  Serial.println("");
//  Serial.println("WiFi connected");
//  Serial.println("IP address: ");
//  Serial.println(WiFi.localIP());
//}
//
//void callback(char* topic, byte* payload, unsigned int length) {
//  Serial.print("Message arrived [");
//  Serial.print(topic);
//  Serial.print("] ");
//  for (int i = 0; i < length; i++) {
//    Serial.print((char)payload[i]);
//  }
//  Serial.println();
//
//  // Switch on the LED if an 1 was received as first character
//  if ((char)payload[0] == 'U') {
//    Serial.print("Up");
//    up();
//    digitalWrite(BUILTIN_LED, HIGH);
//  } 
//  else if ((char)payload[0] == 'D') {
//    Serial.print("Down");
//    down();
//  } 
//  else if ((char)payload[0] == 'L') {
//    Serial.print("Left");
//    left();
//  }
//  else if ((char)payload[0] == 'R') {
//    Serial.print("Right");
//    right();
//  } else {
//    digitalWrite(BUILTIN_LED, LOW);  // Turn the LED off by making the voltage HIGH
//  }
//
//}
//
//void reconnect() {
//  // Loop until we're reconnected
//  while (!client.connected()) {
//    Serial.print("Attempting MQTT connection...");
//    // Attempt to connect
//    if (client.connect("ESP8266Client11",mqttUser, mqttPassword)) {
//      Serial.println("connected");
//      // Once connected, publish an announcement...
//      //client.publish("outTopic", "hello world");
//      // ... and resubscribe
//      client.subscribe("test");
//    } else {
//      Serial.print("failed, rc=");
//      Serial.print(client.state());
//      Serial.println(" try again in 5 seconds");
//      // Wait 5 seconds before retrying
//      delay(5000);
//    }
//  }
//}
//
//void loop() {
//
//  if (!client.connected()) {
//    reconnect();
//  }
//  client.loop();
//
//}
//
//void up(){
//  //digitalWrite();
//  Serial.print("UpUpUp");
//}
//
//void down(){}
//
//void left(){}
//
//void right(){}

