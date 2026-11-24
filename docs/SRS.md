# Software Requirements Specification (SRS)
**Project Title:** Patient Health Monitoring System  
**Framework:** HCLTech Embedded Systems & IoT Project Creation Guide (Step 3 SRS)  
**Author:** Aditya Verma | **Version:** 1.0 (November 2026)

---

## 1. Introduction
This Software Requirements Specification (SRS) defines the functional and non-functional requirements for the **Patient Health Monitoring System**, an educational IoT application designed to monitor, classify, and visualize vital signs in real time.

---

## 2. Functional Requirements (FR)

| Req ID | Requirement Title | Description | Acceptance Criteria |
|:---:|:---|:---|:---|
| **FR-01** | Manual Vital Entry | System shall accept user-entered Heart Rate, SpO2, and Body Temperature. | Prompts for inputs with boundary validation (HR: 1-300, SpO2: 0-100%, Temp: 20-50°C). Rejects non-numeric data. |
| **FR-02** | Excel Ingestion | System shall read tabular patient records from `patient_data.xlsx`. | Validates required schema: `Patient_ID`, `Patient_Name`, `Age`, `Heart_Rate`, `SpO2`, `Temperature`, `Timestamp`. Skips invalid rows without crashing. |
| **FR-03** | Clinical Classification | System shall evaluate parameters against configurable clinical thresholds. | Assigns status per parameter and aggregates overall status: `EMERGENCY` > `CRITICAL` > `WARNING` > `NORMAL`. |
| **FR-04** | Diagnostic Reason Explanation | System shall generate natural language explanations for abnormal vitals. | Outputs specific bullet points explaining why the patient is categorized as WARNING or CRITICAL. |
| **FR-05** | Blynk Cloud Telemetry | System shall transmit vitals to Blynk IoT Cloud using REST API. | Sends HR to V0, SpO2 to V1, Temp to V2, and Status Code (0-3) to V3 via HTTP GET queries. |
| **FR-06** | Emergency Switch Polling | System shall periodically query Blynk Pin V4 state. | Reads Pin V4 every 3 seconds. Detects edge transition ($0 \rightarrow 1$) and triggers visual/audible alarms. |
| **FR-07** | Interactive Web Dashboard | System shall provide a web-based dashboard with live animations. | Renders circular progress gauges, animated Lead II ECG rhythm canvas, emergency SOS toggle, and CSV log download. |
| **FR-08** | Audit Event Logging | System shall log startup checks, evaluations, and alerts to disk. | Writes timestamped records to `logs/monitoring.log` with log levels INFO, WARNING, and CRITICAL. |

---

## 3. Non-Functional Requirements (NFR)

| Req ID | Quality Attribute | Specification |
|:---:|:---|:---|
| **NFR-01** | **Fault Tolerance** | System must continue local monitoring uninterrupted when Blynk Cloud is unreachable or offline. |
| **NFR-02** | **Security & Privacy** | Cloud authentication tokens must never be hard-coded; stored in `.env` and excluded from Git commits. |
| **NFR-03** | **Performance** | Diagnostic processing per patient record shall execute in under 10 ms. |
| **NFR-04** | **Platform Portability** | Pure Python implementation operable across Windows 10/11, macOS, and Linux without native compilers. |
| **NFR-05** | **Test Coverage** | Complete test coverage with 48 unit tests verifying all threshold edge conditions. |

---

## 4. Hardware & Software Constraints
- **Simulation Scope:** In academic simulation mode, no physical sensors or microcontrollers are mandatory.
- **Hardware Integration Roadmap:** System architecture is forward-compatible with ESP32 DevKit v1, MAX30100 PPG sensor, and DS18B20 temperature probe as detailed in the Bill of Materials.
