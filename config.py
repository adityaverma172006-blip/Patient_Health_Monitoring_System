"""
Patient Health Monitoring System - Configuration
=================================================
All configurable thresholds, Blynk settings, and system constants.

This is an educational project for B.Tech college demonstration.
NOT intended for real medical diagnosis.
"""

# =============================================================================
# HEALTH PARAMETER THRESHOLDS
# =============================================================================

# Heart Rate (BPM)
HR_NORMAL_LOW = 60
HR_NORMAL_HIGH = 100
HR_WARNING_LOW = 50
HR_WARNING_HIGH = 110
HR_CRITICAL_LOW = 40
HR_CRITICAL_HIGH = 130

# SpO2 (%)
SPO2_NORMAL = 95
SPO2_WARNING = 90
SPO2_CRITICAL = 85

# Temperature (°C)
TEMP_NORMAL_LOW = 36.0
TEMP_NORMAL_HIGH = 37.5
TEMP_WARNING_HIGH = 38.9
TEMP_CRITICAL_HIGH = 39.0
TEMP_CRITICAL_LOW = 35.0

# =============================================================================
# PATIENT STATUS CODES
# =============================================================================
STATUS_NORMAL = "NORMAL"
STATUS_WARNING = "WARNING"
STATUS_CRITICAL = "CRITICAL"
STATUS_EMERGENCY = "EMERGENCY"

# Numeric codes for Blynk (V3)
STATUS_CODES = {
    STATUS_NORMAL: 0,
    STATUS_WARNING: 1,
    STATUS_CRITICAL: 2,
    STATUS_EMERGENCY: 3,
}

# =============================================================================
# BLYNK VIRTUAL PINS
# =============================================================================
VPIN_HEART_RATE = 0       # V0
VPIN_SPO2 = 1             # V1
VPIN_TEMPERATURE = 2      # V2
VPIN_STATUS = 3           # V3
VPIN_EMERGENCY = 4        # V4

# Blynk Cloud API base URL
BLYNK_API_BASE = "https://blynk.cloud/external/api"

# =============================================================================
# MONITORING SETTINGS
# =============================================================================
MONITORING_INTERVAL = 5          # seconds between automatic readings
EMERGENCY_POLL_INTERVAL = 3      # seconds between emergency switch polls
BLYNK_TIMEOUT = 10               # seconds for API requests

# =============================================================================
# FILE PATHS
# =============================================================================
EXCEL_FILE = "patient_data.xlsx"
LOG_FILE = "logs/monitoring.log"
ENV_FILE = ".env"

# =============================================================================
# SIMULATION DATA
# =============================================================================
SIMULATION_PATIENTS = [
    {
        "patient_id": "P001",
        "patient_name": "Rahul Sharma",
        "age": 28,
        "heart_rate": 82,
        "spo2": 98,
        "temperature": 36.8,
        "condition": "NORMAL",
    },
    {
        "patient_id": "P002",
        "patient_name": "Priya Patel",
        "age": 45,
        "heart_rate": 105,
        "spo2": 92,
        "temperature": 38.2,
        "condition": "WARNING",
    },
    {
        "patient_id": "P003",
        "patient_name": "Amit Kumar",
        "age": 62,
        "heart_rate": 135,
        "spo2": 86,
        "temperature": 39.4,
        "condition": "CRITICAL",
    },
]
