#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT22
#define INTERVAL_SEC 10

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("-- Humidity/Temperature monitor");
  Serial.print("-- Printing every ");
  Serial.print(INTERVAL_SEC);
  Serial.println("s");
  Serial.println("-- Values: H (in %),T (in Celsius)");
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  Serial.print(h);
  Serial.print(",");
  Serial.print(t);
  Serial.print("\n");
  
  delay(10000);
}
