# Wiring Diagram (Text)

```text
[5V PSU]----+----ESP32 5V
            +----LD2410 VCC
            +----HC-SR04 VCC
            +----RCWL-0516 VIN

[Common GND]----ESP32 GND / LD2410 GND / HC-SR04 GND / RCWL GND

LD2410 TX  ---> ESP32 GPIO16 (RX2)
LD2410 RX  <--- ESP32 GPIO17 (TX2)
HC-SR04 TRIG --> ESP32 GPIO5
HC-SR04 ECHO --> ESP32 GPIO18 (level-shifted)
RCWL OUT --> ESP32 GPIO19
```
