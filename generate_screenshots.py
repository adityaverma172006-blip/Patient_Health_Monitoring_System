"""
Screenshot Generator for Patient Health Monitoring System
Generates crisp, high-resolution UI screenshots for college project documentation.
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

def get_font(size, bold=False):
    # Try Windows system fonts
    font_paths = [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_gauge(draw, center, radius, value, min_val, max_val, unit, label, pin, color, bg_ring=(40, 50, 70)):
    cx, cy = center
    # Background arc
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.arc(bbox, start=135, end=405, fill=bg_ring, width=14)
    
    # Value arc
    val_clamped = max(min_val, min(max_val, value))
    pct = (val_clamped - min_val) / (max_val - min_val)
    end_angle = 135 + pct * 270
    draw.arc(bbox, start=135, end=end_angle, fill=color, width=14)
    
    # Texts
    font_val = get_font(32, bold=True)
    font_unit = get_font(14)
    font_lbl = get_font(13, bold=True)
    font_pin = get_font(11)
    
    # Draw label & pin
    draw.text((cx, cy - radius - 25), label, fill=(180, 195, 215), font=font_lbl, anchor="mm")
    draw.text((cx, cy - radius - 8), f"PIN {pin}", fill=(6, 182, 212), font=font_pin, anchor="mm")
    
    # Draw value
    val_str = f"{value:.1f}" if isinstance(value, float) else f"{value}"
    draw.text((cx, cy - 5), val_str, fill=(245, 248, 255), font=font_val, anchor="mm")
    draw.text((cx, cy + 22), unit, fill=(140, 155, 175), font=font_unit, anchor="mm")

def create_blynk_screenshot(filename, hr, spo2, temp, status, switch_on, patient_name, patient_id):
    width, height = 1100, 680
    img = Image.new("RGB", (width, height), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Fonts
    f_title = get_font(22, bold=True)
    f_sub = get_font(13)
    f_card_title = get_font(14, bold=True)
    f_body = get_font(13)
    
    # Top Navbar (Blynk Console style)
    draw.rectangle([0, 0, width, 65], fill=(30, 41, 59))
    draw.line([0, 65, width, 65], fill=(51, 65, 85), width=1)
    
    # Blynk Logo / Brand
    draw.rounded_rectangle([25, 16, 60, 48], radius=6, fill=(34, 197, 94))
    draw.text((42, 32), "B", fill=(255, 255, 255), font=get_font(20, bold=True), anchor="mm")
    draw.text((75, 24), "Blynk.Cloud  /  Device Dashboard", fill=(241, 245, 249), font=f_title)
    draw.text((75, 47), "Template: Patient Health Monitor • Online (Hardware / Cloud REST API)", fill=(148, 163, 184), font=f_sub)
    
    # Device State Pill
    draw.rounded_rectangle([width - 160, 20, width - 25, 48], radius=14, fill=(22, 101, 52))
    draw.ellipse([width - 145, 30, width - 135, 40], fill=(74, 222, 128))
    draw.text((width - 85, 34), "CONNECTED", fill=(240, 253, 244), font=get_font(12, bold=True), anchor="mm")
    
    # Patient Banner
    draw.rounded_rectangle([25, 85, width - 25, 145], radius=12, fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((45, 105), f"Active Patient: {patient_id} — {patient_name}", fill=(248, 250, 252), font=get_font(16, bold=True))
    draw.text((45, 126), "Telemetry Stream: Live Virtual Pins V0, V1, V2, V3, V4 • Mode: Cloud REST API Polling", fill=(148, 163, 184), font=f_sub)
    
    # Status Pill on Banner
    status_colors = {
        "NORMAL": ((16, 185, 129), (6, 78, 59)),
        "WARNING": ((245, 158, 11), (120, 53, 15)),
        "CRITICAL": ((239, 68, 68), (127, 29, 29)),
        "EMERGENCY": ((236, 72, 153), (131, 24, 67)),
    }
    fg_col, bg_col = status_colors.get(status, ((16, 185, 129), (6, 78, 59)))
    draw.rounded_rectangle([width - 210, 100, width - 45, 132], radius=16, fill=bg_col, outline=fg_col, width=1)
    draw.text((width - 128, 116), f"STATUS: {status}", fill=fg_col, font=get_font(13, bold=True), anchor="mm")
    
    # Grid of 4 Widget Cards
    card_w = (width - 25 * 5) // 4
    card_y = 165
    card_h = 240
    
    # 1. Heart Rate (V0)
    c1_x = 25
    draw.rounded_rectangle([c1_x, card_y, c1_x + card_w, card_y + card_h], radius=12, fill=(30, 41, 59), outline=(51, 65, 85))
    hr_color = (239, 68, 68) if hr > 130 or hr < 40 else ((245, 158, 11) if hr > 100 or hr < 60 else (16, 185, 129))
    draw_gauge(draw, (c1_x + card_w // 2, card_y + 130), 65, hr, 40, 180, "BPM", "Heart Rate Gauge", "V0", hr_color)
    
    # 2. SpO2 (V1)
    c2_x = c1_x + card_w + 25
    draw.rounded_rectangle([c2_x, card_y, c2_x + card_w, card_y + card_h], radius=12, fill=(30, 41, 59), outline=(51, 65, 85))
    spo2_color = (239, 68, 68) if spo2 < 90 else ((245, 158, 11) if spo2 <= 94 else (16, 185, 129))
    draw_gauge(draw, (c2_x + card_w // 2, card_y + 130), 65, spo2, 70, 100, "%", "SpO2 Oxygen Gauge", "V1", spo2_color)
    
    # 3. Temperature (V2)
    c3_x = c2_x + card_w + 25
    draw.rounded_rectangle([c3_x, card_y, c3_x + card_w, card_y + card_h], radius=12, fill=(30, 41, 59), outline=(51, 65, 85))
    temp_color = (239, 68, 68) if temp >= 39.0 or temp < 35.0 else ((245, 158, 11) if temp > 37.5 else (16, 185, 129))
    draw_gauge(draw, (c3_x + card_w // 2, card_y + 130), 65, temp, 34.0, 42.0, "°C", "Temperature Gauge", "V2", temp_color)
    
    # 4. Emergency Switch (V4)
    c4_x = c3_x + card_w + 25
    draw.rounded_rectangle([c4_x, card_y, c4_x + card_w, card_y + card_h], radius=12, fill=(30, 41, 59), outline=(236, 72, 153) if switch_on else (51, 65, 85))
    draw.text((c4_x + card_w // 2, card_y + 35), "Emergency Switch", fill=(244, 114, 182), font=f_card_title, anchor="mm")
    draw.text((c4_x + card_w // 2, card_y + 55), "PIN V4", fill=(6, 182, 212), font=get_font(11), anchor="mm")
    
    # Toggle Graphic
    sw_y = card_y + 115
    sw_w, sw_h = 90, 46
    sw_x = c4_x + (card_w - sw_w) // 2
    if switch_on:
        draw.rounded_rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + sw_h], radius=23, fill=(236, 72, 153))
        draw.ellipse([sw_x + sw_w - 42, sw_y + 4, sw_x + sw_w - 6, sw_y + 42], fill=(255, 255, 255))
        draw.text((c4_x + card_w // 2, card_y + 185), "ACTIVATED (1)", fill=(244, 114, 182), font=get_font(15, bold=True), anchor="mm")
        draw.text((c4_x + card_w // 2, card_y + 210), "SOS ALARM ACTIVE", fill=(239, 68, 68), font=get_font(11, bold=True), anchor="mm")
    else:
        draw.rounded_rectangle([sw_x, sw_y, sw_x + sw_w, sw_y + sw_h], radius=23, fill=(51, 65, 85))
        draw.ellipse([sw_x + 6, sw_y + 4, sw_x + 42, sw_y + 42], fill=(148, 163, 184))
        draw.text((c4_x + card_w // 2, card_y + 185), "STANDBY (0)", fill=(148, 163, 184), font=get_font(15, bold=True), anchor="mm")
        draw.text((c4_x + card_w // 2, card_y + 210), "Normal Monitoring", fill=(100, 116, 139), font=get_font(11), anchor="mm")
    
    # Bottom Panel: Diagnostics & Rest API Log
    bot_y = 430
    bot_h = 220
    draw.rounded_rectangle([25, bot_y, width - 25, bot_y + bot_h], radius=12, fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((45, bot_y + 25), "Cloud Telemetry & Clinical Reasoning (Virtual Pin V3 Details)", fill=(248, 250, 252), font=get_font(15, bold=True))
    
    # Code block look
    draw.rounded_rectangle([45, bot_y + 50, width - 45, bot_y + bot_h - 25], radius=8, fill=(15, 23, 42), outline=(51, 65, 85))
    
    lines = [
        f"[HTTP GET] https://blynk.cloud/external/api/update?token=***&pin=V0&value={hr}  --> 200 OK",
        f"[HTTP GET] https://blynk.cloud/external/api/update?token=***&pin=V1&value={spo2}  --> 200 OK",
        f"[HTTP GET] https://blynk.cloud/external/api/update?token=***&pin=V2&value={temp} --> 200 OK",
        f"[HTTP GET] https://blynk.cloud/external/api/update?token=***&pin=V3&value={'2' if status=='CRITICAL' else ('1' if status=='WARNING' else '0')} --> 200 OK (Status={status})",
        f"[HTTP GET] https://blynk.cloud/external/api/get?token=***&pin=V4 --> 200 OK [Response: '{'1' if switch_on else '0'}']"
    ]
    if status == "CRITICAL":
        lines.append(f"!!! CRITICAL ALERT: Heart rate abnormal ({hr} BPM), SpO2 critically low ({spo2}%), High fever ({temp}°C) !!!")
    
    curr_y = bot_y + 60
    for l in lines:
        col = (239, 68, 68) if "CRITICAL" in l or "1" in l and "V4" in l else ((34, 197, 94) if "200 OK" in l else (203, 213, 225))
        draw.text((60, curr_y), l, fill=col, font=get_font(12))
        curr_y += 24
        
    img.save(f"screenshots/{filename}", quality=95)
    print(f"Created screenshots/{filename}")

def create_terminal_screenshot():
    width, height = 950, 620
    img = Image.new("RGB", (width, height), (12, 12, 12))
    draw = ImageDraw.Draw(img)
    
    # Terminal Top Bar
    draw.rectangle([0, 0, width, 36], fill=(35, 35, 35))
    # Close / Min / Max dots
    draw.ellipse([15, 12, 27, 24], fill=(255, 95, 86))
    draw.ellipse([35, 12, 47, 24], fill=(255, 189, 46))
    draw.ellipse([55, 12, 67, 24], fill=(39, 201, 63))
    draw.text((width // 2, 18), "Administrator: Windows PowerShell — python main.py", fill=(180, 180, 180), font=get_font(12), anchor="mm")
    
    # Terminal text
    term_font = get_font(13)
    term_bold = get_font(13, bold=True)
    
    content = [
        ("PS C:\\Users\\hp\\Patient_Health_Monitoring_System> .\\venv\\Scripts\\Activate.ps1", (200, 200, 200)),
        ("(venv) PS C:\\Users\\hp\\Patient_Health_Monitoring_System> python main.py", (255, 255, 255)),
        ("", (0,0,0)),
        ("==================================================", (6, 182, 212)),
        ("   PATIENT HEALTH MONITORING SYSTEM", (255, 255, 255)),
        ("   Educational IoT Project", (150, 150, 150)),
        ("==================================================", (6, 182, 212)),
        ("", (0,0,0)),
        ("--- Startup Check ---", (255, 255, 255)),
        ("  [OK] Python 3.14.0", (34, 197, 94)),
        ("  [OK] Environment file found (.env)", (34, 197, 94)),
        ("  [OK] Blynk token configured (a8f4****2b91)", (34, 197, 94)),
        ("  [OK] Blynk connection successful.", (34, 197, 94)),
        ("  [OK] Excel file found (patient_data.xlsx)", (34, 197, 94)),
        ("  [OK] Logs directory ready", (34, 197, 94)),
        ("--------------------------------------------------", (100, 100, 100)),
        ("", (0,0,0)),
        ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", (239, 68, 68)),
        ("        CRITICAL CONDITION DETECTED", (239, 68, 68)),
        ("        Patient: P003 (Amit Kumar)", (255, 255, 255)),
        ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", (239, 68, 68)),
        ("  Heart Rate   : 135.0 BPM [CRITICAL]", (239, 68, 68)),
        ("  SpO2         : 86.0% [CRITICAL]", (239, 68, 68)),
        ("  Temperature  : 39.4°C [CRITICAL]", (239, 68, 68)),
        ("  Overall Status: CRITICAL", (239, 68, 68)),
        ("  Reasons:", (255, 255, 255)),
        ("    - Heart rate is critically abnormal (135 BPM).", (245, 158, 11)),
        ("    - Oxygen level is critically low (86%).", (245, 158, 11)),
        ("    - Temperature is critically high (39.4°C).", (245, 158, 11)),
        ("  Blynk: Data sent to Blynk ✓", (34, 197, 94)),
    ]
    
    y = 50
    for text, color in content:
        draw.text((25, y), text, fill=color, font=term_font)
        y += 18
        
    img.save("screenshots/terminal_monitoring_demo.png", quality=95)
    print("Created screenshots/terminal_monitoring_demo.png")

def create_web_dashboard_screenshot():
    width, height = 1100, 720
    img = Image.new("RGB", (width, height), (11, 17, 32))
    draw = ImageDraw.Draw(img)
    
    # Top Educational Banner
    draw.rectangle([0, 0, width, 32], fill=(30, 58, 138))
    draw.text((width // 2, 16), "⚕️ Academic Project: Patient Health Monitoring System — Live Web Dashboard & Telemetry Stream", fill=(191, 219, 254), font=get_font(12, bold=True), anchor="mm")
    
    # Header card
    draw.rounded_rectangle([25, 45, width - 25, 115], radius=12, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.ellipse([45, 60, 85, 100], fill=(239, 68, 68))
    draw.text((65, 80), "❤️", fill=(255, 255, 255), font=get_font(18), anchor="mm")
    
    draw.text((100, 68), "Patient Health Monitoring System — Live IoT Dashboard", fill=(243, 244, 246), font=get_font(17, bold=True))
    draw.text((100, 92), "Patient: P001 — Rahul Sharma (Age 28) | Updated: 10:15:32 AM | Port: 5000", fill=(156, 163, 175), font=get_font(12))
    
    # Status Pill
    draw.rounded_rectangle([width - 170, 65, width - 45, 95], radius=15, fill=(6, 78, 59), outline=(16, 185, 129))
    draw.text((width - 108, 80), "● NORMAL", fill=(52, 211, 153), font=get_font(13, bold=True), anchor="mm")
    
    # Controls row
    draw.rounded_rectangle([25, 128, width - 25, 168], radius=8, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.rounded_rectangle([35, 134, 175, 162], radius=6, fill=(37, 99, 235))
    draw.text((105, 148), "Patient 1 (Normal)", fill=(255, 255, 255), font=get_font(11, bold=True), anchor="mm")
    
    draw.rounded_rectangle([185, 134, 325, 162], radius=6, fill=(31, 41, 55))
    draw.text((255, 148), "Patient 2 (Warning)", fill=(209, 213, 219), font=get_font(11), anchor="mm")
    
    draw.rounded_rectangle([335, 134, 475, 162], radius=6, fill=(31, 41, 55))
    draw.text((405, 148), "Patient 3 (Critical)", fill=(209, 213, 219), font=get_font(11), anchor="mm")
    
    draw.rounded_rectangle([485, 134, 650, 162], radius=6, fill=(31, 41, 55), outline=(16, 185, 129))
    draw.text((567, 148), "⚡ Auto Simulation: ON", fill=(52, 211, 153), font=get_font(11, bold=True), anchor="mm")
    
    # Grid of 4 Cards
    cw = (width - 25 * 5) // 4
    cy = 180
    ch = 190
    
    # Card 1: HR
    draw.rounded_rectangle([25, cy, 25 + cw, cy + ch], radius=10, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.text((40, cy + 20), "HEART RATE", fill=(156, 163, 175), font=get_font(11, bold=True))
    draw.text((25 + cw - 40, cy + 20), "PIN V0", fill=(6, 182, 212), font=get_font(10))
    draw.text((40, cy + 65), "82", fill=(243, 244, 246), font=get_font(36, bold=True))
    draw.text((95, cy + 80), "BPM", fill=(156, 163, 175), font=get_font(13))
    draw.rounded_rectangle([40, cy + 120, 25 + cw - 40, cy + 128], radius=4, fill=(55, 65, 81))
    draw.rounded_rectangle([40, cy + 120, 40 + int((cw - 80) * 0.35), cy + 128], radius=4, fill=(16, 185, 129))
    draw.text((40, cy + 145), "Normal Range: 60 - 100 BPM", fill=(107, 114, 128), font=get_font(10))
    
    # Card 2: SpO2
    c2 = 25 + cw + 25
    draw.rounded_rectangle([c2, cy, c2 + cw, cy + ch], radius=10, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.text((c2 + 15, cy + 20), "OXYGEN SATURATION", fill=(156, 163, 175), font=get_font(11, bold=True))
    draw.text((c2 + cw - 40, cy + 20), "PIN V1", fill=(6, 182, 212), font=get_font(10))
    draw.text((c2 + 15, cy + 65), "98", fill=(243, 244, 246), font=get_font(36, bold=True))
    draw.text((c2 + 70, cy + 80), "%", fill=(156, 163, 175), font=get_font(13))
    draw.rounded_rectangle([c2 + 15, cy + 120, c2 + cw - 15, cy + 128], radius=4, fill=(55, 65, 81))
    draw.rounded_rectangle([c2 + 15, cy + 120, c2 + int((cw - 30) * 0.98), cy + 128], radius=4, fill=(16, 185, 129))
    draw.text((c2 + 15, cy + 145), "Normal Range: ≥ 95%", fill=(107, 114, 128), font=get_font(10))
    
    # Card 3: Temp
    c3 = c2 + cw + 25
    draw.rounded_rectangle([c3, cy, c3 + cw, cy + ch], radius=10, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.text((c3 + 15, cy + 20), "BODY TEMPERATURE", fill=(156, 163, 175), font=get_font(11, bold=True))
    draw.text((c3 + cw - 40, cy + 20), "PIN V2", fill=(6, 182, 212), font=get_font(10))
    draw.text((c3 + 15, cy + 65), "36.8", fill=(243, 244, 246), font=get_font(36, bold=True))
    draw.text((c3 + 100, cy + 80), "°C", fill=(156, 163, 175), font=get_font(13))
    draw.rounded_rectangle([c3 + 15, cy + 120, c3 + cw - 15, cy + 128], radius=4, fill=(55, 65, 81))
    draw.rounded_rectangle([c3 + 15, cy + 120, c3 + int((cw - 30) * 0.45), cy + 128], radius=4, fill=(16, 185, 129))
    draw.text((c3 + 15, cy + 145), "Normal Range: 36.0 - 37.5°C", fill=(107, 114, 128), font=get_font(10))
    
    # Card 4: Emergency Switch
    c4 = c3 + cw + 25
    draw.rounded_rectangle([c4, cy, c4 + cw, cy + ch], radius=10, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.text((c4 + 15, cy + 20), "EMERGENCY SWITCH", fill=(244, 114, 182), font=get_font(11, bold=True))
    draw.text((c4 + cw - 40, cy + 20), "PIN V4", fill=(236, 72, 153), font=get_font(10))
    draw.text((c4 + 15, cy + 65), "OFF", fill=(156, 163, 175), font=get_font(32, bold=True))
    draw.text((c4 + 90, cy + 78), "(0)", fill=(107, 114, 128), font=get_font(13))
    # Toggle button
    draw.rounded_rectangle([c4 + 15, cy + 115, c4 + 80, cy + 145], radius=15, fill=(55, 65, 81))
    draw.ellipse([c4 + 20, cy + 118, c4 + 44, cy + 142], fill=(209, 213, 219))
    draw.text((c4 + 95, cy + 130), "Standby", fill=(156, 163, 175), font=get_font(11), anchor="lm")
    
    # Middle: Real-Time ECG Waveform Lead II
    ecg_y = 385
    ecg_h = 130
    draw.rounded_rectangle([25, ecg_y, width - 25, ecg_y + ecg_h], radius=10, fill=(5, 10, 20), outline=(6, 182, 212), width=1)
    draw.text((40, ecg_y + 18), "REAL-TIME ECG / RHYTHM LEAD II", fill=(6, 182, 212), font=get_font(11, bold=True))
    draw.text((width - 45, ecg_y + 18), "25 mm/s | Filtered (0.5 - 40 Hz)", fill=(107, 114, 128), font=get_font(10), anchor="ra")
    
    # Draw simulated ECG pulse path
    mid_y = ecg_y + 70
    points = []
    x = 35
    while x < width - 35:
        # PQRST complex
        points.append((x, mid_y))
        points.append((x + 20, mid_y))
        points.append((x + 25, mid_y - 8))  # P wave
        points.append((x + 30, mid_y))
        points.append((x + 40, mid_y))
        points.append((x + 44, mid_y + 6))  # Q wave
        points.append((x + 48, mid_y - 45)) # R wave
        points.append((x + 52, mid_y + 14)) # S wave
        points.append((x + 58, mid_y))
        points.append((x + 72, mid_y - 12)) # T wave
        points.append((x + 80, mid_y))
        x += 110
    
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(6, 182, 212), width=2)
        
    # Bottom: Diagnostics list
    diag_y = 530
    diag_h = 160
    draw.rounded_rectangle([25, diag_y, width - 25, diag_y + diag_h], radius=10, fill=(17, 24, 39), outline=(55, 65, 81))
    draw.text((40, diag_y + 18), "Clinical Diagnostic Breakdown (Status V3 = 0 [NORMAL])", fill=(243, 244, 246), font=get_font(12, bold=True))
    
    diag_items = [
        ("✓ All physiological parameters within normal baseline clinical range.", (52, 211, 153)),
        ("✓ Heart Rate: 82 BPM (Normal range: 60 - 100 BPM)", (209, 213, 219)),
        ("✓ Blood Oxygen SpO2: 98% (Normal range: ≥ 95%)", (209, 213, 219)),
        ("✓ Body Temperature: 36.8°C (Normal range: 36.0 - 37.5°C)", (209, 213, 219)),
        ("✓ Emergency Switch: Inactive (V4 = 0)", (209, 213, 219)),
    ]
    dy = diag_y + 45
    for item, icol in diag_items:
        draw.text((50, dy), item, fill=icol, font=get_font(11))
        dy += 21
        
    img.save("screenshots/live_web_dashboard.png", quality=95)
    print("Created screenshots/live_web_dashboard.png")

if __name__ == "__main__":
    # 1. Blynk Dashboard Normal
    create_blynk_screenshot("blynk_dashboard_normal.png", 82, 98, 36.8, "NORMAL", False, "Rahul Sharma", "P001")
    # 2. Blynk Dashboard Critical
    create_blynk_screenshot("blynk_dashboard_critical.png", 135, 86, 39.4, "CRITICAL", True, "Amit Kumar", "P003")
    # 3. Terminal Screenshot
    create_terminal_screenshot()
    # 4. Live Web Dashboard
    create_web_dashboard_screenshot()
    print("All screenshots generated successfully!")
