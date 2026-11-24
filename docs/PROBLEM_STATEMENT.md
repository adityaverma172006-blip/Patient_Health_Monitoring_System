# Problem Statement — Patient Health Monitoring System
**Course:** HCLTech BTech Embedded Systems & IoT | **Document:** Step 1 Problem Statement

---

## 1. Executive Summary
Continuous patient monitoring is a cornerstone of modern clinical care. However, standard clinical practices in general wards and home-quarantine environments rely on periodic nursing rounds conducted every 4 to 6 hours. During the intervals between observations, patient conditions can deteriorate sharply due to unobserved cardiac arrhythmias, hypoxemic crises, or malignant hyperthermia.

## 2. Core Problem Definition
1. **Latency in Acute Event Detection:** Intermittent manual vital sign readings fail to provide early-warning signals for rapid acute deteriorations.
2. **High Infrastructure & Equipment Costs:** Clinical ICU bedside telemetry units cost thousands of dollars per bed, which severely limits widespread deployment in developing regions or pre-clinical student labs.
3. **Delayed Alert Notification:** Standard bedside alarms produce localized acoustic signals that are easily missed when attendants are attending to other rooms.
4. **Data Fragmentation:** Paper-based or isolated monitor readings lack synchronized cloud logging for trend analysis and historical review.

## 3. Scope of Solution
Build an educational, cost-effective, and robust IoT-based Patient Health Monitoring System using Python, Blynk IoT Cloud, and an interactive Web Dashboard:
- Ingest vital signs via Manual Input, Excel (`patient_data.xlsx`), or continuous physiological simulation.
- Real-time assessment of Heart Rate (BPM), Blood Oxygen Saturation ($SpO_2$ %), and Body Temperature (°C).
- Automated condition classification (`NORMAL`, `WARNING`, `CRITICAL`, and `EMERGENCY`).
- Low-latency cloud telemetry dispatch via REST API.
- Non-blocking edge polling of a patient emergency panic button (Blynk Pin `V4`).
- Visual and audible multi-parameter web dashboard with animated Lead II ECG waveform.

## 4. Target Users
- Hospital recovery ward staff requiring centralized vital sign tracking.
- Home-isolated patients under remote clinical supervision.
- BTech engineering students and IoT researchers prototyping biomedical telemetry systems.

## 5. Success Metrics
- **Classification Accuracy:** 100% agreement with standard clinical threshold criteria across 48 automated test cases.
- **Latency:** Core evaluation and condition categorization executed in < 10 ms.
- **Resilience:** Graceful offline degradation when internet or Blynk Cloud services are disconnected.
