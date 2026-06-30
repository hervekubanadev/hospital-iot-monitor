# API Reference

## Daemon Commands

### `python3 hospital_system.py start`

Starts the hospital sensor simulation daemon in the background.

**Behaviour:**
- Forks into background process
- Writes PID to `/tmp/hospital_system.pid`
- Begins writing sensor data every 1 second to `active_logs/`
- Logs to three files: `heart_rate_log.log`, `temperature_log.log`, `water_usage_log.log`

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Daemon started successfully |
| 1 | Daemon already running (PID file exists) |

**Example:**
```bash
python3 hospital_system.py start
# Output: Hospital Management System started (PID: 12345).
```

---

### `python3 hospital_system.py stop`

Gracefully stops the running daemon.

**Behaviour:**
- Sends SIGTERM to the tracked PID
- Removes the PID file
- Leaves existing log data intact

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Daemon stopped successfully |
| 0 | No running daemon found |

**Example:**
```bash
python3 hospital_system.py stop
# Output: Hospital Management System stopped.
```

---

## Admin Commands

### `bash hospital_admin.sh`

Initialises the monitoring environment and applies security controls.

**Operations:**
1. Creates `active_logs/` directory (if absent)
2. Creates `archived_logs/` directory (if absent)
3. Creates `reports/` directory (if absent)
4. Applies `chmod 700` to `active_logs/`

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Environment initialised successfully |

**Example:**
```bash
bash hospital_admin.sh
```

---

## Analysis Commands

### `bash hospital_analysis.sh`

Analyses current log data and generates reports.

**Operations:**
1. Extracts all CRITICAL entries from `heart_rate_log.log` and `temperature_log.log`
2. Writes them to `reports/critical_alerts.txt`
3. Computes average ICU_WATER_RESERVE consumption from `water_usage_log.log`

**Output Files:**

| File | Content |
|------|---------|
| `reports/critical_alerts.txt` | Timestamped critical vital sign events |

**Example:**
```bash
bash hospital_analysis.sh
# Output: Critical alerts were properly saved to reports/critical_alerts.txt
```

---

## Archive Commands

### `bash hospital_archive.sh`

Rotates active log files into timestamped archives.

**Operations:**
1. Moves each `.log` file from `active_logs/` to `archived_logs/`
2. Appends timestamp suffix: `{basename}_YYYYMMDD_HHMM.log`
3. Creates fresh empty log files in `active_logs/`

**Example:**
```bash
bash hospital_archive.sh
# Output: Archiving heart_rate_log.log to archived_logs/heart_rate_log_20260630_1430.log
```

---

## Sensor Data Formats

### Heart Rate Log

```
Timestamp | Device_ID | Heart_Rate (BPM) | Status
2026-06-30 14:30:01 | WARD_A_HR_01 | 72 | NORMAL
```

### Temperature Log

```
Timestamp | Device_ID | Temperature (Celsius) | Status
2026-06-30 14:30:01 | WARD_B_TEMP_03 | 38.2 | CRITICAL
```

### Water Usage Log

```
Timestamp | Device_ID | Usage (Liters/min) | Status
2026-06-30 14:30:01 | ICU_WATER_RESERVE | 28 | NORMAL
```

---

## Status Codes

| Status | Meaning | Applicable Sensors |
|--------|---------|-------------------|
| NORMAL | Reading within safe range | All |
| WARNING | Approaching threshold | Heart Rate |
| CRITICAL | Outside safe range | Heart Rate, Temperature |
| HIGH_USAGE | Exceeding water consumption limit | Water Meters |
