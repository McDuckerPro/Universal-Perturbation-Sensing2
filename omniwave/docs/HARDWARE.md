# OmniWave Hardware Integration Guide

## Bill of Materials (MVP)
- ESP32 DevKit v1 (USB powered, 5V)
- HLK-LD2410 or S3KM111L 24GHz radar
- HC-SR04 ultrasonic sensor
- RCWL-0516 microwave motion module
- Jumper wires, breadboard, 5V 2A supply

## Pin mapping (example)
- LD2410 TX -> ESP32 RX2 (GPIO16)
- LD2410 RX -> ESP32 TX2 (GPIO17)
- HC-SR04 TRIG -> GPIO5
- HC-SR04 ECHO -> GPIO18 (use divider to 3.3V)
- RCWL-0516 OUT -> GPIO19
- GND common between all modules

## Power requirements
- ESP32 via USB 5V
- LD2410 at 5V (check module board regulator)
- HC-SR04 at 5V
- RCWL-0516 at 4-28V (commonly 5V)
- Keep total rail current under supply rating; recommend >=2A adapter.

## JSON line serial protocol
Firmware emits newline-delimited JSON:
```json
{"sensor_type":"radar_ld2410","sample_rate":10,"channels":1,"bins":2,"data":[[0.10,0.22]],"metadata":{"firmware":"omniwave-mvp"}}
```

## PlatformIO flashing
1. Install VS Code + PlatformIO extension.
2. Open `firmware/esp32`.
3. Select `esp32dev` environment.
4. Build and upload.
5. Open serial monitor at 115200 baud and confirm JSON lines.
