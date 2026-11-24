# Bill of Materials (BOM) — Hardware Integration Roadmap
**Project:** Patient Health Monitoring System  
**Track:** HCLTech Embedded Systems & IoT | **Document:** Section 5 Bill of Materials (BOM)

---

## Hardware Component Specification

| S.No | Component / Part Description | Qty | Unit Cost (INR) | Total Cost (INR) | Supplier | Purpose in System |
|:---:|:---|:---:|:---:|:---:|:---|:---|
| **1** | **ESP32 DevKit v1 (30-pin Dual-Core Microcontroller)** | 1 | 450 | 450 | Robu.in | Primary edge controller with built-in Wi-Fi and Bluetooth BLE. |
| **2** | **MAX30100 Pulse Oximeter & Heart Rate PPG Sensor** | 1 | 240 | 240 | Amazon India | Reads Heart Rate (BPM) and Blood Oxygen ($SpO_2$ %) via I2C. |
| **3** | **DS18B20 Waterproof Digital Body Temperature Sensor** | 1 | 180 | 180 | Robu.in | Reads clinical body temperature (°C) via OneWire bus. |
| **4** | **0.96" I2C 128x64 OLED Display (SSD1306)** | 1 | 180 | 180 | Robu.in | Bedside visual display of live vitals and status badge. |
| **5** | **Emergency Push Button (Red Momentary Switch with Resistor)** | 1 | 30 | 30 | Local Electronics | Physical bedside panic switch mapped to Virtual Pin V4. |
| **6** | **Piezo Buzzer (5V Active Alarm Buzzer)** | 1 | 25 | 25 | Local Electronics | Audible bedside alarm on CRITICAL or EMERGENCY conditions. |
| **7** | **5V 2A Regulated Micro-USB Power Supply Adapter** | 1 | 250 | 250 | Amazon India | Reliable power source for continuous 24/7 bedside operation. |
| **8** | **Full-sized Breadboard + 40-pin Jumper Wire Ribbon** | 1 | 150 | 150 | Local Electronics | Prototyping interconnects and ground/power rail distribution. |
| | **TOTAL ESTIMATED HARDWARE PROTOTYPE COST** | | | **1,505 INR** | | |

---

## Pin Mapping Table (ESP32 DevKit v1)

| Sensor / Actuator | Sensor Pin | ESP32 GPIO Pin | Protocol / Interface |
|:---|:---:|:---:|:---|
| MAX30100 PPG Sensor | `SDA` | `GPIO 21` | I2C Data |
| MAX30100 PPG Sensor | `SCL` | `GPIO 22` | I2C Clock |
| DS18B20 Temp Probe | `DATA` | `GPIO 4` | OneWire Bus (4.7kΩ pull-up) |
| 0.96" OLED Display | `SDA` / `SCL` | `GPIO 21` / `GPIO 22` | Shared I2C Bus |
| Emergency Panic Switch | `SIGNAL` | `GPIO 15` | Digital Input with Pull-down |
| Piezo Buzzer | `POSITIVE` | `GPIO 18` | Digital Output (PWM capable) |
| Power Rails | `VCC` / `GND` | `3V3` / `5V` / `GND` | Power & Ground |
