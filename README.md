# Patient Health Monitoring System

> [!WARNING]
> **Academic Project Disclaimer**  
> This is an educational project for academic purposes. It is NOT intended for real medical diagnosis or patient care.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Blynk IoT](https://img.shields.io/badge/Blynk-IoT%20Cloud%20REST%20API-00B06F.svg)](https://blynk.io/)
[![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458.svg)](https://pandas.pydata.org/)
[![OpenPyXL](https://img.shields.io/badge/Excel-OpenPyXL-217346.svg)](https://openpyxl.readthedocs.io/)
[![License: Educational](https://img.shields.io/badge/License-Educational-green.svg)](#)

---

## Table of Contents

1. [Project Title & Overview](#patient-health-monitoring-system)
2. [Abstract](#abstract)
3. [Problem Statement](#problem-statement)
4. [Project Objectives](#project-objectives)
5. [Key Features](#key-features)
6. [Hardware Requirements](#hardware-requirements)
7. [Software Requirements](#software-requirements)
8. [Technologies Used](#technologies-used)
9. [Project Directory Structure](#project-directory-structure)
10. [System Architecture](#system-architecture)
11. [Working Principle](#working-principle)
12. [Python Implementation Details](#python-implementation-details)
13. [Health Parameter Thresholds & Evaluation Logic](#health-parameter-thresholds--evaluation-logic)
14. [Excel Integration](#excel-integration)
15. [Blynk IoT Cloud Integration](#blynk-iot-cloud-integration)
16. [Virtual Pins Mapping](#virtual-pins-mapping)
17. [Emergency Switch Mechanism](#emergency-switch-mechanism)
18. [Blynk Cloud Dashboard Setup Guide](#blynk-cloud-dashboard-setup-guide)
19. [Installation Steps (Windows)](#installation-steps-windows)
20. [How to Run & Menu Walkthrough](#how-to-run--menu-walkthrough)
21. [Testing Instructions](#testing-instructions)
22. [System Limitations](#system-limitations)
23. [Future Improvements](#future-improvements)
24. [Conclusion](#conclusion)
25. [Viva Questions and Answers (20 Q&A Pairs)](#viva-questions-and-answers)

---

## Abstract

The **Patient Health Monitoring System** is a software-driven Internet of Things (IoT) simulation system designed for remote patient vitals monitoring and emergency response. Developed in Python with integration to the Blynk Cloud IoT platform, this academic project demonstrates how real-time physiological indicators—specifically **Heart Rate (BPM)**, **Blood Oxygen Saturation ($SpO_2$)**, and **Body Temperature (°C)**—can be ingested, evaluated against clinical classification thresholds, and visualized on cloud-connected dashboards without demanding dedicated physical biomedical hardware during initial prototyping.

The system features robust batch processing via Microsoft Excel (`patient_data.xlsx`), interactive terminal telemetry inputs, automated multi-patient round-robin simulation, bidirectional cloud communication with state-change detection for an emergency panic switch, and structured audit logging. It serves as an end-to-end blueprint for students and researchers exploring tele-health architectures, clinical decision support algorithms, and cloud telemetry integration.

---

## Problem Statement

Modern healthcare facilities frequently face challenges related to resource allocation, patient overcrowding, and delayed intervention during sudden vital sign deterioration in unmonitored recovery wards. In conventional setups:

1. **Intermittent Manual Checks:** Hospital staff record vital signs periodically (often every 4–6 hours), missing abrupt cardiac arrhythmias or hypoxic events between intervals.
2. **Geographical & Mobility Constraints:** Rural or home-quarantined patients lack immediate access to centralized hospital telemetry units.
3. **High Deployment Costs:** Clinical-grade patient telemetry monitoring hardware carries prohibitive capital expenses, making widespread pre-deployment and student experimentation challenging.
4. **Delayed Emergency Triggers:** Bedside alarms frequently remain localized to the room, creating latency in alerting remote medical attendants or emergency teams.

There is a compelling need for a lightweight, accessible, cross-platform telemetry framework that bridges localized patient vital sign acquisition with low-latency cloud transmission, visual condition categorization, and immediate emergency signaling.

---

## Project Objectives

The primary engineering and educational goals of this project include:

1. **Design a Unified Telemetry Ingestion Engine:** Build an interactive terminal-based interface supporting validated manual entries, batch Excel inputs, and automated simulation data loops.
2. **Implement Multi-Parameter Clinical Threshold Evaluation:** Develop modular algorithms to evaluate Heart Rate, $SpO_2$, and Temperature against standard medical threshold boundaries (`NORMAL`, `WARNING`, and `CRITICAL`).
3. **Synthesize Overall Patient Condition:** Implement deterministic multi-tier prioritization logic where the single most severe vital abnormality drives the composite patient status.
4. **Integrate with Blynk Cloud IoT Platform:** Establish REST API communication using HTTP GET requests for bi-directional telemetry transmission and status updates without third-party heavy brokers.
5. **Implement Remote Emergency Switch Polling:** Continually monitor a cloud-based emergency panic button (Blynk Virtual Pin `V4`) with real-time edge/state-change detection.
6. **Support Batch Patient Records with Excel:** Leverage Pandas and OpenPyXL to ingest, validate, and bulk-assess structured clinical datasets.
7. **Ensure System Fault Tolerance & Offline Graceful Degradation:** Maintain full diagnostic assessment and logging locally even when internet connectivity or the IoT cloud is unreachable.
8. **Facilitate Automated Verification:** Provide a comprehensive unit test suite covering parameter evaluation, edge conditions, boundary logic, and mock service behaviors.

---

## Key Features

- **Multi-Source Data Ingestion:**
  - *Manual Input Mode:* Interactive, validated console prompts for real-time one-off vital sign assessment.
  - *Excel Ingestion Mode:* Reads structured patient records from `.xlsx` files with automatic schema validation and type parsing.
  - *Simulation Mode:* Automated cycles cycling through predetermined healthy, borderline, and emergency clinical profiles.
- **Dynamic Condition Categorization:**
  - Multi-tier classification for Heart Rate, $SpO_2$, and Body Temperature.
  - Generates human-readable clinical rationale explaining which parameter breached boundaries.
- **Bidirectional Blynk Cloud IoT Integration:**
  - Real-time synchronous dispatch of telemetry parameters to Blynk Virtual Pins `V0`, `V1`, `V2`, and `V3`.
  - Asynchronous / polling-based retrieval of cloud-triggered emergency commands via Virtual Pin `V4`.
- **Emergency Panic Button Detection:**
  - Continuous background monitoring loop that alerts operators upon instant switch activation ($0 \rightarrow 1$).
- **Structured Audit Logging:**
  - Persistent timestamps, severity levels, and diagnostic trace events captured to `logs/monitoring.log`.
- **Fault-Tolerant Network Fallback:**
  - Clear visual notices when cloud services are unreachable; the system never crashes or halts core calculations due to lost internet.
- **Automated Startup Sanity Checks:**
  - Validates Python runtime, `.env` authentication credentials, local file access, and cloud ping on boot.

---

## Hardware Requirements

Because this project features an intelligent **Simulation Engine** and validated software inputs, specialized biomedical sensors or microcontrollers are not mandatory for running and evaluating the system.

- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher (Dual-Core 2.0 GHz+).
- **Memory (RAM):** 4 GB RAM minimum (8 GB recommended for multi-tasking).
- **Storage:** 500 MB free hard disk space.
- **Network Interface:** Active Wi-Fi or Ethernet internet connection (required for Blynk Cloud REST API updates).
- **Input Device:** Standard Keyboard and Monitor / Display.
- *(Optional for Future Hardware Deployment):* ESP32 / Arduino Uno, MAX30100/MAX30102 Pulse Oximeter sensor, DS18B20 Digital Temperature probe, and USB-UART cable.

---

## Software Requirements

- **Operating System:** Microsoft Windows 10/11, macOS 10.15+, or Ubuntu/Debian Linux.
- **Python Runtime:** Python 3.8, 3.9, 3.10, 3.11, or 3.12 (64-bit recommended).
- **Code Editor / IDE:** Visual Studio Code, PyCharm, or any text editor with terminal access.
- **IoT Cloud Account:** Free tier account on [Blynk.Cloud](https://blynk.cloud/).
- **Web Browser:** Google Chrome, Mozilla Firefox, or Microsoft Edge for managing the Blynk Web Console dashboard.
- **Spreadsheet Viewer:** Microsoft Excel, LibreOffice Calc, or Google Sheets (to generate or view `patient_data.xlsx`).

---

## Technologies Used

| Technology | Role & Purpose |
|:---|:---|
| **Python 3** | Core language for business logic, threshold evaluation, and CLI orchestration. |
| **Pandas** | High-performance data manipulation and parsing of tabular patient records. |
| **OpenPyXL** | Read/write interface supporting Excel `.xlsx` file manipulation. |
| **Requests** | Robust HTTP library utilized for dispatching RESTful API queries to the Blynk Cloud. |
| **python-dotenv** | Secure environment configuration loader ensuring auth tokens remain out of source control. |
| **Blynk Cloud REST API** | Low-latency cloud ingestion interface exposing endpoints for pin read/update operations. |
| **Pytest / Unittest** | Test automation framework for unit verification of clinical evaluation boundaries. |

---

## Project Directory Structure

```text
Patient_Health_Monitoring_System/
│
├── .env                              # Local environment file containing BLYNK_AUTH_TOKEN (ignored by git)
├── .env.example                      # Template demonstrating required environment keys
├── .gitignore                        # Git exclusion rules for venv, cache, logs, and secrets
├── requirements.txt                  # Python package dependency specifications
├── config.py                         # System-wide configuration, thresholds, pin mappings, and constants
├── patient_monitor.py                # Core medical evaluation, thresholding, and console display logic
├── blynk_service.py                  # HTTP client encapsulating Blynk Cloud REST API communication
├── excel_service.py                  # Service for reading, writing, and validating Excel spreadsheets
├── main.py                           # CLI entry point, startup diagnostic checks, and interactive menu
├── patient_data.xlsx                 # Primary Excel spreadsheet storing tabular patient health records
│
├── logs/
│   └── monitoring.log                # Rolling log file storing system activity and clinical alerts
│
└── tests/
    └── test_patient_monitor.py       # Unit test suite verifying logic, thresholds, and service modules
```

---

## System Architecture

The following diagram illustrates the flow of patient data from diverse input channels through the validation and classification engine, culminating in local output displays and cloud dashboard telemetry:

```text
+-------------------------------------------------------------------------------+
|                             DATA INGESTION SOURCES                            |
+-------------------------------------------------------------------------------+
       |                                       |                                |
       v                                       v                                v
 [ Manual Input ]                    [ patient_data.xlsx ]            [ Simulation Engine ]
 (Keyboard Terminal)                  (Pandas / OpenPyXL)             (Predefined Profiles)
       |                                       |                                |
       +---------------------------------------+--------------------------------+
                                               |
                                               v
                        +---------------------------------------------+
                        |      PATIENT HEALTH MONITORING CORE         |
                        |            (patient_monitor.py)             |
                        +---------------------------------------------+
                        | 1. Sanitize & Validate Numeric Ranges       |
                        | 2. Compare against Clinical Thresholds:    |
                        |    - Heart Rate (BPM)                       |
                        |    - SpO2 Saturation (%)                    |
                        |    - Body Temperature (°C)                  |
                        | 3. Determine Overall Severity:              |
                        |    [NORMAL] < [WARNING] < [CRITICAL]        |
                        +---------------------------------------------+
                                      |                     |
                  +-------------------+                     +-------------------+
                  |                                                             |
                  v                                                             v
+------------------------------------+                        +------------------------------------+
|          LOCAL OUTPUTS             |                        |         BLYNK CLOUD IoT            |
+------------------------------------+                        +------------------------------------+
| 1. Formatted Console Display       |                        | 1. REST API Dispatch:              |
|    - Parameter Status Tags         |                        |    - V0: Heart Rate                |
|    - Clinical Explanation Flags    |                        |    - V1: SpO2                      |
| 2. File Audit Trail                |                        |    - V2: Temperature               |
|    - logs/monitoring.log           |                        |    - V3: Overall Status (0-3)      |
|    - Persistent Alert Tracing      |                        | 2. Polling Loop:                   |
+------------------------------------+                        |    - V4: Emergency Button Polling  |
                                                              +------------------------------------+
                                                                                |
                                                                                v
                                                              +------------------------------------+
                                                              |       WEB & MOBILE DASHBOARD       |
                                                              +------------------------------------+
                                                              | - Real-time Gauges (V0, V1, V2)    |
                                                              | - Numerical Condition Widget (V3)  |
                                                              | - Panic Alert Switch Widget (V4)   |
                                                              +------------------------------------+
```

---

## Working Principle

1. **Telemetry Ingestion:** The user selects a data acquisition mode from the interactive CLI: manual console input, batch Excel workbook reading, or continuous simulated stream generation.
2. **Numeric Validation:** The input values are validated to ensure they conform to plausible human biological envelopes:
   - Heart Rate: $1 \le \text{BPM} \le 300$
   - $SpO_2$: $0\% \le \text{Oxygen} \le 100\%$
   - Temperature: $20.0^\circ\text{C} \le \text{Temp} \le 50.0^\circ\text{C}$
3. **Threshold Assessment:** Individual parameters are mapped against established medical thresholds:
   - Evaluated as `NORMAL`, `WARNING`, or `CRITICAL`.
   - Any deviation from standard physiological parameters appends a diagnostic descriptive reason (e.g., *"Oxygen level is critically low (86%)"*).
4. **Composite Status Resolution:** The system calculates a unified patient status via hierarchical prioritization:
   $$\text{Overall Status} = \max(\text{Status}_{\text{HR}}, \text{Status}_{\text{SpO2}}, \text{Status}_{\text{Temp}})$$
   Where $\text{CRITICAL} > \text{WARNING} > \text{NORMAL}$.
5. **Local Telemetry & Audit Dispatch:** Results are formatted into a clean terminal report with colorized demarcation lines and written out to `logs/monitoring.log` with microsecond-level timestamps.
6. **Cloud Synchronization:** If configured, the telemetry client issues synchronous HTTP GET requests to the Blynk Cloud REST API, updating Virtual Pins `V0`, `V1`, `V2`, and `V3`.
7. **Emergency State Detection:** In dedicated emergency mode, the application queries Blynk Virtual Pin `V4`. When an operator toggles the widget from $0 \rightarrow 1$, a high-priority interrupt is flagged across local consoles and system logs.

---

## Python Implementation Details

The codebase adheres strictly to clean code principles, modular encapsulation, and separation of concerns across five key Python modules:

### 1. `config.py`
Serves as the single source of truth for the entire application. It contains:
- Clinical threshold boundaries for heart rate, oxygen saturation, and temperature.
- Status code string enumerations (`NORMAL`, `WARNING`, `CRITICAL`, `EMERGENCY`) and their numeric mapping for Blynk transmission (`0`, `1`, `2`, `3`).
- Blynk Cloud API base endpoint (`https://blynk.cloud/external/api`) and Virtual Pin definitions (`VPIN_HEART_RATE = 0`, etc.).
- Timing constants (`MONITORING_INTERVAL = 5`, `EMERGENCY_POLL_INTERVAL = 3`, `BLYNK_TIMEOUT = 10`).
- Preconfigured mock patient profiles for deterministic test simulations.

### 2. `patient_monitor.py`
Encapsulates all medical evaluation algorithms and terminal presentation logic:
- `evaluate_heart_rate(hr)`: Evaluates heart rate and returns a tuple `(status, reason)`.
- `evaluate_spo2(spo2)`: Assesses blood oxygen saturation percentage against hypoxia thresholds.
- `evaluate_temperature(temp)`: Checks body temperature for hypothermia or fever/hyperpyrexia.
- `calculate_overall_status(hr_s, spo2_s, temp_s)`: Applies priority logic ($\text{CRITICAL} \succ \text{WARNING} \succ \text{NORMAL}$).
- `evaluate_patient(hr, spo2, temp)`: Runs the complete assessment pipeline, compiles diagnostic reasons, timestamps the reading, and emits structured log events.
- `display_patient_result(...)`: Formats and prints banner-highlighted status cards to the console.
- `get_manual_patient_data()`: Provides interactive CLI prompts with strict boundary checks and error reprompting.

### 3. `blynk_service.py`
Manages all cloud networking using the lightweight Blynk Cloud REST API:
- `BlynkService.__init__()`: Safely loads the authentication token from `.env` via `python-dotenv`.
- `is_configured()` & `get_masked_token()`: Returns safe token strings (e.g., `9abc****3xyz`) to prevent credentials from being exposed in screen recordings or viva presentations.
- `check_connection()`: Hits `/external/api/isHardwareConnected` to confirm active cloud availability.
- `update_pin(pin, value)`: Updates a virtual pin using `/external/api/update?token={token}&pin=V{pin}&value={value}`.
- `get_pin(pin)`: Reads an integer/string value from `/external/api/get?token={token}&pin=V{pin}`.
- `send_patient_data(hr, spo2, temp, status_code)`: Batch-dispatches all 4 telemetry streams sequentially, compiling an aggregate success indicator.
- `get_emergency_switch()`: Queries Virtual Pin `V4`, parsing the response into state `0` or `1`.

### 4. `excel_service.py`
Provides spreadsheet input/output abstraction via `pandas` and `openpyxl`:
- `REQUIRED_COLUMNS`: Enforces validation against mandatory columns: `Patient_ID`, `Patient_Name`, `Age`, `Heart_Rate`, `SpO2`, `Temperature`, `Timestamp`.
- `create_sample_excel(filepath)`: Automatically creates a sample `patient_data.xlsx` workbook populated with representative healthy, warning, and critical profiles if no file exists.
- `read_patient_data(filepath)`: Validates file presence, verifies column headers, parses each row, runs numeric checks, skips corrupted rows gracefully, and yields a clean list of patient dictionaries.

### 5. `main.py`
The primary application orchestrator:
- Bootstraps console logging to `logs/monitoring.log`.
- `startup_check()`: Verifies Python runtime, inspects environment keys, tests cloud reachability, and auto-generates default Excel workbooks if missing.
- Implements the interactive CLI menu loop supporting all 8 core options.
- Manages graceful shutdown on `KeyboardInterrupt` (`Ctrl+C`) and unexpected exception containment.

---

## Health Parameter Thresholds & Evaluation Logic

The following clinical categorization logic is modeled in `config.py` and evaluated within `patient_monitor.py`:

| Parameter | Normal Range | Warning Range | Critical Range | Units |
|:---|:---:|:---:|:---:|:---:|
| **Heart Rate** | $60 - 100$ | $50 - 59$ OR $101 - 110$ | $< 40$ OR $> 130$ | Beats Per Minute (BPM) |
| **Oxygen Saturation ($SpO_2$)** | $\ge 95\%$ | $90\% - 94\%$ | $< 90\%$ | Percentage (%) |
| **Body Temperature** | $36.0 - 37.5$ | $37.6 - 38.9$ | $\ge 39.0$ OR $< 35.0$ | Degrees Celsius (°C) |

### Overall Status Derivation Priority
```text
IF any parameter is CRITICAL  ===> Overall Status = CRITICAL  (Blynk Code: 2)
ELSE IF any is WARNING        ===> Overall Status = WARNING   (Blynk Code: 1)
ELSE                          ===> Overall Status = NORMAL    (Blynk Code: 0)
```
*(Emergency Switch Override: When Virtual Pin $V4 = 1$, status translates to `EMERGENCY` / Blynk Code: 3).*

---

## Excel Integration

The system integrates directly with Microsoft Excel `.xlsx` files using `pandas` and `openpyxl`. This allows clinicians or researchers to supply large cohorts of patient readings for automated batch evaluation.

### File Specifications
- **Filename:** `patient_data.xlsx`
- **Default Location:** Project root directory.
- **Required Columns:**

| Column Name | Data Type | Example Value | Description |
|:---|:---:|:---:|:---|
| `Patient_ID` | String | `P001` | Unique alphanumeric patient record identifier |
| `Patient_Name` | String | `Rahul Sharma` | Full name of the patient |
| `Age` | Integer | `28` | Patient age in years |
| `Heart_Rate` | Float / Int | `82` | Recorded pulse rate in BPM |
| `SpO2` | Float / Int | `98` | Peripheral blood oxygen percentage |
| `Temperature` | Float | `36.8` | Core body temperature in °C |
| `Timestamp` | String / DateTime | `2026-11-20 10:00:00` | Reading capture timestamp |

### Robust Error Handling in Excel Reading
- If `patient_data.xlsx` is missing on boot, `excel_service.create_sample_excel()` automatically initializes a valid template file.
- If individual rows contain non-numeric entries or empty fields, the system prints a notification, skips the corrupted entry, and continues processing remaining records.
- At the end of batch processing, the operator is prompted with an option to publish the final evaluated record directly to Blynk Cloud.

---

## Blynk IoT Cloud Integration

Rather than requiring complex MQTT broker setups or specialized embedded libraries, this project communicates with Blynk Cloud via lightweight, stateless HTTP GET requests against the Blynk External REST API.

### Endpoints Used

#### 1. Hardware Connection Check
- **Endpoint:** `GET /external/api/isHardwareConnected`
- **Query Parameters:** `token={BLYNK_AUTH_TOKEN}`
- **Response:** `true` (if online / active token), `false` (if offline), or HTTP 401 (invalid auth token).

#### 2. Update Virtual Pin Value
- **Endpoint:** `GET /external/api/update`
- **Query Parameters:** `token={BLYNK_AUTH_TOKEN}&pin=V{pin_number}&value={value}`
- **Response:** HTTP `200 OK` on successful write.

#### 3. Read Virtual Pin Value
- **Endpoint:** `GET /external/api/get`
- **Query Parameters:** `token={BLYNK_AUTH_TOKEN}&pin=V{pin_number}`
- **Response:** Returns JSON string array containing the pin's current value (e.g. `["1"]`).

---

## Virtual Pins Mapping

The project maps all vital telemetry streams, clinical status indicators, and emergency controls to designated Blynk Virtual Pins:

| Virtual Pin | Parameter Name | Data Type | Min Value | Max Value | Default Widget Type | Description |
|:---:|:---|:---:|:---:|:---:|:---|:---|
| **`V0`** | Heart Rate | Integer | `0` | `300` | Radial Gauge | Patient Pulse in Beats Per Minute (BPM) |
| **`V1`** | $SpO_2$ | Integer | `0` | `100` | Radial Gauge | Oxygen Saturation Level (%) |
| **`V2`** | Temperature | Double | `20.0` | `50.0` | Radial Gauge | Body Temperature in Celsius (°C) |
| **`V3`** | Patient Status | Integer | `0` | `3` | Value Display / Label | `0`=NORMAL, `1`=WARNING, `2`=CRITICAL, `3`=EMERGENCY |
| **`V4`** | Emergency Switch | Integer | `0` | `1` | Push Switch / Button | `0`=Standby / OFF, `1`=Emergency Active |

---

## Emergency Switch Mechanism

Virtual Pin `V4` functions as a bidirectional emergency panic alert. This simulates a patient bedside panic switch or a doctor remote override button.

```text
[ Blynk App / Web Dashboard ]
              |
       (User toggles V4)
              |
              v
     Blynk Cloud Server (V4 = 1)
              |
              |  GET /external/api/get?token=...&pin=V4
              v
[ Python Monitoring Loop: option_emergency_switch() ]
              |
    Checks: Is current_state != last_state?
              |
    +---------+---------+
    |                   |
 (State == 1)        (State == 0)
    |                   |
    v                   v
[ CRITICAL LOG & ALERT ] [ Standby Log ]
 "EMERGENCY SWITCH        "Emergency switch
  ACTIVATED (V4 = ON)!"    deactivated."
```

### Key Technical Aspects:
1. **Periodic Non-Blocking Polling:** The system queries Blynk Cloud every `config.EMERGENCY_POLL_INTERVAL` (default: 3 seconds).
2. **State-Change Edge Detection:** Audio-visual triggers fire only on edge transitions ($0 \rightarrow 1$ or $1 \rightarrow 0$), preventing redundant terminal spam while continuously verifying heartbeat.
3. **Audit Logging:** Every transition is immediately registered in `logs/monitoring.log` under `CRITICAL` or `INFO` log levels.

---

## Blynk Cloud Dashboard Setup Guide

Follow these exact steps to configure your Blynk Cloud IoT console for this project:

### Step 1: Create Account & Workspace
1. Navigate to [blynk.cloud](https://blynk.cloud/) and create a free account.
2. Log in and access the **Blynk Console**.

### Step 2: Create a Device Template
1. From the left sidebar, click **Templates** (Developer Zone) $\rightarrow$ **+ New Template**.
2. Set the following fields:
   - **Name:** `Patient Health Monitor`
   - **Hardware:** `Other` (or `ESP32` / `ESP8266`)
   - **Connection Type:** `Wi-Fi` / `Ethernet`
3. Click **Done**.

### Step 3: Configure Datastreams
Go to the **Datastreams** tab within your newly created template, click **+ New Datastream** $\rightarrow$ **Virtual Pin** for each of the 5 datastreams below:

| Datastream Name | Pin | Data Type | Min | Max | Default |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Heart Rate** | `V0` | Integer | `0` | `300` | `0` |
| **SpO2** | `V1` | Integer | `0` | `100` | `0` |
| **Temperature** | `V2` | Double (0.1 precision) | `20` | `50` | `36.5` |
| **Status** | `V3` | Integer | `0` | `3` | `0` |
| **Emergency Switch** | `V4` | Integer | `0` | `1` | `0` |

*Click **Save** in the top right corner to persist datastreams.*

### Step 4: Provision a Device
1. Click the **Search** icon (Magnifying glass) on the main sidebar $\rightarrow$ **+ New Device**.
2. Select **From template**.
3. Choose the `Patient Health Monitor` template.
4. Set the device name to `Patient 01` and click **Create**.
5. Locate the **Device Info** tab:
   - Copy the **Auth Token** (a 32-character alphanumeric string, e.g. `ab7x92Kla8194kd82103kdp19283746a`).

### Step 5: Configure Local Environment
1. In the project directory, open `.env` (or copy from `.env.example`).
2. Paste your copied token:
   ```bash
   BLYNK_AUTH_TOKEN=your_copied_blynk_auth_token_here
   ```

### Step 6: Construct the Web Dashboard
1. Inside your template or device view, navigate to **Web Dashboard** $\rightarrow$ **Edit**.
2. Drag and drop the following UI widgets onto your canvas:
   - **Gauge 1:** Datastream = `Heart Rate (V0)`, Title = "Heart Rate", Range = `0 - 300 BPM`, Color = Orange/Red.
   - **Gauge 2:** Datastream = `SpO2 (V1)`, Title = "Blood Oxygen (SpO2)", Range = `0 - 100 %`, Color = Cyan/Blue.
   - **Gauge 3:** Datastream = `Temperature (V2)`, Title = "Body Temperature", Range = `20 - 50 °C`, Color = Green.
   - **Value Display:** Datastream = `Status (V3)`, Title = "Clinical Status", Color = Purple.
   - **Switch / Button:** Datastream = `Emergency Switch (V4)`, Title = "Emergency Trigger", Mode = `Switch`.
3. Click **Save And Apply**.

---

## Installation Steps (Windows)

Follow these exact commands in Windows PowerShell or Command Prompt to set up and run the environment:

### 1. Open Project Directory
Launch VS Code and open the project directory:
```powershell
cd C:\Users\hp\.gemini\antigravity\scratch\Patient_Health_Monitoring_System
```

### 2. Create Virtual Environment
Create a dedicated virtual environment named `venv`:
```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment
- **In PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(Note: If execution scripts are restricted on your system, enable them for this session by running: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

- **In Command Prompt (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```

### 4. Install Dependencies
Install all required libraries specified in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 5. Configure Authentication Token
Copy the template and insert your Blynk authentication token:
```powershell
copy .env.example .env
```
Open `.env` in VS Code or Notepad and set:
```ini
BLYNK_AUTH_TOKEN=YOUR_ACTUAL_BLYNK_TOKEN_HERE
```

### 6. Run the Application
Execute the primary script:
```powershell
python main.py
```

---

## How to Run & Menu Walkthrough

When you start the system (`python main.py`), the program executes automated diagnostic checks and displays the main interactive dashboard:

```text
==================================================
   PATIENT HEALTH MONITORING SYSTEM
   Educational IoT Project
==================================================

--- Startup Check ---

  [OK] Python 3.11.x
  [OK] Environment file found (.env)
  [OK] Blynk token configured (9a8b****1z9x)
  [OK] Blynk connection successful.
  [OK] Excel file found (patient_data.xlsx)
  [OK] Logs directory ready

--------------------------------------------------

==================================================
                  MAIN MENU
==================================================
  1. Enter patient data manually
  2. Read patient data from Excel
  3. Test normal/warning/critical conditions
  4. Monitor Blynk emergency switch
  5. Start automatic monitoring
  6. View latest patient data
  7. Check Blynk connection
  8. Exit
==================================================
  Enter your choice (1-8):
```

### Step-by-Step Menu Features:

#### Option 1: Enter Patient Data Manually
- **Action:** Prompts the user to enter Heart Rate, $SpO_2$, and Temperature with real-time numeric bounds validation.
- **Output:** Renders an evaluated clinical report card and automatically syncs values to the Blynk Cloud.
- **Console Preview:**
  ```text
  --------------------------------------------------
          PATIENT MONITORING
          Patient: Manual Entry
  --------------------------------------------------

    Heart Rate   : 75.0 BPM [NORMAL]
    SpO2         : 98.0% [NORMAL]
    Temperature  : 36.6°C [NORMAL]

    Overall Status: NORMAL
    Timestamp     : 2026-11-20 10:15:30
  ```

#### Option 2: Read Patient Data from Excel
- **Action:** Ingests rows from `patient_data.xlsx`, assesses each patient, displays formatted evaluation cards for each entry, and prompts to push the final patient record to the cloud.

#### Option 3: Test Conditions (Simulation Benchmark)
- **Action:** Iterates sequentially through 3 pre-built medical benchmarks:
  1. *Rahul Sharma* (Healthy baseline $\rightarrow$ `NORMAL`)
  2. *Priya Patel* (Elevated temperature, mild hypoxia $\rightarrow$ `WARNING`)
  3. *Amit Kumar* (Tachycardia, critical hypoxia, high fever $\rightarrow$ `CRITICAL`)

#### Option 4: Monitor Blynk Emergency Switch
- **Action:** Enters an active listening loop querying Blynk Pin `V4`. When the switch is toggled ON in the Blynk app or Web Console, an emergency alert banner flashes across the screen:
  ```text
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !!! EMERGENCY SWITCH ACTIVATED (V4 = ON) !!!
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  ```
- Press `Ctrl+C` to return cleanly to the main menu.

#### Option 5: Start Automatic Monitoring
- **Action:** Emulates continuous real-time clinical telemetry by cycling through simulation profiles every 5 seconds, recalculating status, updating logs, and transmitting data to Blynk Cloud.

#### Option 6: View Latest Patient Data
- **Action:** Re-displays the most recently evaluated patient record without requiring new inputs.

#### Option 7: Check Blynk Connection
- **Action:** Performs an on-demand connectivity test against `https://blynk.cloud/external/api/isHardwareConnected` and displays connection latency and token masking status.

#### Option 8: Exit
- **Action:** Flushes remaining log buffers, closes connections gracefully, and terminates the session.

---

## Testing Instructions

The repository includes a comprehensive unit test suite in `tests/test_patient_monitor.py` built upon Python's native `unittest` framework.

### Running Tests with Pytest
To run the automated suite with verbose outputs using pytest:
```powershell
python -m pytest tests/test_patient_monitor.py -v
```

### Running Tests with Python Unittest
Alternatively, run directly using the standard library:
```powershell
python -m unittest tests/test_patient_monitor.py -v
```

### Test Coverage Highlights
- `TestHeartRateEvaluation`: Verifies normal range ($60-100$), edge boundary values ($60$, $100$), mild warning conditions ($55$, $105$), extreme critical levels ($35$, $140$), and handling of invalid/null types.
- `TestSpO2Evaluation`: Verifies normoxia ($\ge 95\%$), hypoxemia warnings ($90-94\%$), and severe hypoxia ($< 90\%$).
- `TestTemperatureEvaluation`: Verifies normal apyrexia ($36.0-37.5^\circ\text{C}$), low-grade fever ($38.2^\circ\text{C}$), hyperpyrexia ($39.4^\circ\text{C}$), and hypothermia ($34.0^\circ\text{C}$).
- `TestOverallStatus`: Asserts condition hierarchy ($\text{CRITICAL} \succ \text{WARNING} \succ \text{NORMAL}$).
- `TestExcelService`: Tests automated creation of sample workbooks, reading dataframes, missing file detection, and column schema validation.
- `TestBlynkService`: Confirms token masking, unconfigured fallback safety, and zero-network error isolation.

---

## System Limitations

1. **Simulated Telemetry:** The project utilizes simulation profiles, manual console entries, and Excel datasets; it does not connect directly to live human biomedical sensors in this stage.
2. **Not a Certified Medical Device:** This software is engineered strictly for educational demonstrations and must NOT be used for actual clinical diagnostics, life-support, or patient triage.
3. **Discrete Telemetry Polling:** Communication with Blynk relies on HTTP REST requests rather than a continuous microsecond WebSocket or MQTT streaming socket.
4. **No Persistent Relational Database:** Records are managed in flat files (`.xlsx` and `.log`) rather than an ACID-compliant SQL or NoSQL database (such as PostgreSQL or MongoDB).
5. **Network Dependency for Cloud Features:** While local monitoring operates completely offline, IoT remote dashboard synchronization and emergency switch polling require active internet connectivity.

---

## Future Improvements

1. **Physical Microcontroller Integration:** Interface an **ESP32** or **Arduino Nano 33 IoT** via Wi-Fi or Serial (UART) to transmit physiological signals from real sensors.
2. **Biomedical Sensor Interfacing:**
   - **MAX30100 / MAX30102:** Optical sensor for Photoplethysmography (PPG), pulse oximetry ($SpO_2$), and heart rate.
   - **DS18B20 / MLX90614:** Digital contact or infrared non-contact body temperature sensing.
   - **AD8232:** 3-lead single-channel electrocardiogram (ECG) heart activity monitor.
3. **Enterprise Database Storage:** Replace flat Excel files with an embedded SQLite or PostgreSQL database for historical telemetry archiving and query optimization.
4. **Machine Learning Predictive Analytics:** Train supervised machine learning models (e.g., Random Forest or LSTM recurrent neural networks) to predict early onset of septic shock or cardiac arrest from vital trends.
5. **Omnichannel Alerting:** Integrate Twilio or SendGrid APIs to dispatch automated SMS, WhatsApp, and email alerts directly to on-call physicians when `CRITICAL` or `EMERGENCY` events are detected.
6. **Progressive Web App (PWA):** Build a dedicated React.js or Flutter mobile/web dashboard with secure user authentication and multi-bed hospital ward views.

---

## Conclusion

The **Patient Health Monitoring System** successfully showcases how modern software engineering and accessible cloud IoT services can converge to solve critical challenges in remote healthcare telemetry. By decoupling vital sign acquisition, clinical rule evaluation, and cloud visualization, the system achieves a modular, robust, and extensible architecture.

Through comprehensive edge-case validation, Excel batch ingestion, fail-safe local operations, and bidirectional Blynk Cloud REST API communication, this project fulfills all foundational objectives of an undergraduate B.Tech engineering project, laying a clear path for future hardware and machine-learning enhancements.

---

## Viva Questions and Answers

Here are 20 foundational questions and answers prepared specifically for academic project evaluations, external examiners, and technical viva voce presentations:

### Q1: What is IoT?
**A:** IoT (Internet of Things) is an interconnected network of physical devices, vehicles, appliances, and medical instruments embedded with sensors, software, network connectivity, and processing units that enable them to collect, exchange, and act on data across the internet without requiring direct human-to-computer interaction.

### Q2: What is Patient Health Monitoring?
**A:** Patient Health Monitoring is a medical telemetry system that continuously or periodically tracks a patient's core physiological vital signs—such as heart rate, oxygen saturation ($SpO_2$), body temperature, and blood pressure—enabling healthcare professionals to detect abnormal conditions early, monitor recovery, and initiate immediate clinical interventions.

### Q3: Why Python for this project?
**A:** Python offers rapid prototyping capabilities, clean syntax, cross-platform portability, and a comprehensive ecosystem of libraries. Libraries like `pandas` and `openpyxl` make data manipulation effortless, while `requests` enables clean, readable HTTP communication with cloud APIs.

### Q4: Why Blynk for IoT?
**A:** Blynk provides a robust, developer-friendly cloud infrastructure with a built-in REST API, customizable mobile and web visualization widgets, and fast setup without requiring manual cloud server provisioning, firewall routing, or database configuration.

### Q5: What is a REST API?
**A:** A REST (Representational State Transfer) API is an architectural style for networked web services. It uses standard HTTP verbs (such as `GET`, `POST`, `PUT`, `DELETE`) and stateless request-response transactions to transfer structured data (frequently JSON or text) between clients and servers.

### Q6: What is a Virtual Pin in Blynk?
**A:** A Virtual Pin in Blynk is a software-defined communication channel that acts as a bridge between the physical device/application and the Blynk Cloud. Unlike physical GPIO pins that control voltage high/low, Virtual Pins can transmit integers, floating-point numbers, strings, and multi-value arrays to UI widgets.

### Q7: What is SpO2?
**A:** $SpO_2$ stands for Peripheral Oxygen Saturation. It measures the percentage of oxygen-saturated hemoglobin relative to total hemoglobin in the blood. A healthy adult typically displays readings between $95\%$ and $100\%$. Levels below $90\%$ represent clinical hypoxemia requiring immediate medical attention.

### Q8: How is heart rate measured in real systems?
**A:** In practical biomedical hardware, heart rate is measured using Photoplethysmography (PPG) sensors like the MAX30100 or MAX30102. These sensors emit red and infrared light through the vascular tissue of a fingertip or earlobe and measure variations in light absorption caused by pulsing arterial blood volume.

### Q9: How does the system calculate patient status?
**A:** The system evaluates each parameter (Heart Rate, $SpO_2$, Temperature) independently against predefined medical ranges, labeling each as `NORMAL`, `WARNING`, or `CRITICAL`. It then executes a priority hierarchy: if any parameter is `CRITICAL`, the overall status becomes `CRITICAL`; if none are critical but at least one is `WARNING`, the overall status is `WARNING`; otherwise, it is `NORMAL`.

### Q10: What is the Excel file used for?
**A:** The Excel file (`patient_data.xlsx`) stores structured historical or cohort patient records comprising Patient ID, Name, Age, and vital signs. It enables the system to perform automated batch processing and multi-patient evaluations without requiring manual re-entry of data.

### Q11: How does the emergency switch work?
**A:** The emergency switch is mapped to Blynk Virtual Pin `V4`. The Python backend periodically polls this pin via an HTTP GET request. When the widget on the Blynk dashboard is toggled ON ($V4 = 1$), the application registers a state-change edge, prints a high-priority visual alert banner to the terminal, and flags a critical entry in the system log.

### Q12: How does Python communicate with Blynk?
**A:** Python utilizes the `requests` library to issue standard HTTP GET requests to the Blynk Cloud REST API endpoints (`/external/api/update` to write virtual pin values, and `/external/api/get` to read virtual pin values) authenticated via a unique Device Auth Token.

### Q13: What happens when Blynk goes offline?
**A:** The system is engineered with robust exception handling (`requests.exceptions.RequestException`). If Blynk Cloud is unreachable or the internet drops, the system logs a warning, alerts the user, and continues local evaluation, terminal display, and file logging without crashing or halting execution.

### Q14: What is simulation mode?
**A:** Simulation mode is a software mechanism that cycles through representative, predefined clinical patient datasets (normal, warning, critical). It allows complete verification and demonstration of system behavior, algorithm logic, and cloud telemetry synchronization without needing physical hardware or live patients.

### Q15: What are the system's limitations?
**A:** Key limitations include reliance on simulated rather than continuous biological sensor signals, lack of certification as a regulated clinical diagnostic tool, dependence on active internet connectivity for remote features, and reliance on flat files (`.xlsx`) rather than a transactional relational database.

### Q16: How can physical sensors be integrated?
**A:** An external microcontroller like an ESP32 or Arduino can be interfaced with physical sensors (e.g., MAX30100 for pulse/$SpO_2$ and DS18B20 for temperature). The microcontroller can read sensor registers via $I^2C$ or 1-Wire protocols and forward the digitized readings to this Python application via USB Serial (UART) or directly over Wi-Fi via HTTP/MQTT.

### Q17: What is the role of the .env file?
**A:** The `.env` file securely stores sensitive configuration variables—specifically the `BLYNK_AUTH_TOKEN`—outside the codebase. This follows industry best practices (Twelve-Factor App methodology), preventing private authentication credentials from being committed to public version control systems like GitHub.

### Q18: What libraries does this project use?
**A:** The project uses:
- `pandas` for tabular data ingestion and manipulation.
- `openpyxl` as the spreadsheet engine for reading/writing `.xlsx` workbooks.
- `requests` for RESTful HTTP network interactions with Blynk Cloud.
- `python-dotenv` for loading secrets from environment files.
- `pytest` / `unittest` for automated test suite execution.

### Q19: What is the difference between WARNING and CRITICAL status?
**A:** A `WARNING` status denotes vital signs that deviate moderately from normal baselines (e.g., elevated temperature of $38.2^\circ\text{C}$ or mild hypoxia with $92\% SpO_2$), signaling the need for close observation. A `CRITICAL` status signifies life-threatening physiological deviations (e.g., severe hypoxia $< 90\% SpO_2$, heart rate $> 130$ BPM, or hyperpyrexia $\ge 39.0^\circ\text{C}$) requiring immediate medical intervention.

### Q20: How would you improve this project in the future?
**A:** Key improvements include:
1. Interfacing physical biomedical hardware (MAX30102 and DS18B20 on an ESP32).
2. Implementing an encrypted PostgreSQL or MongoDB backend for longitudinal health records.
3. Building automated SMS and phone call alerts using the Twilio API.
4. Integrating Machine Learning algorithms to analyze time-series telemetry trends for early anomaly prediction.
5. Deploying a comprehensive Web/Mobile Progressive Web App (PWA) with role-based doctor/nurse access.
