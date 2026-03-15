#include <Arduino.h>

// MVP firmware stub for OmniWave JSON line protocol
// Replace mock values with real sensor reads from LD2410 / HC-SR04 / RCWL0516.

unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (millis() - lastSend > 100) {
    lastSend = millis();
    float d0 = random(0, 100) / 100.0;
    float d1 = random(0, 100) / 100.0;
    Serial.print("{\"sensor_type\":\"radar_ld2410\",\"sample_rate\":10,\"channels\":1,\"bins\":2,\"data\":[[");
    Serial.print(d0, 3);
    Serial.print(",");
    Serial.print(d1, 3);
    Serial.println("]],\"metadata\":{\"firmware\":\"omniwave-mvp\"}}");
  }
}
