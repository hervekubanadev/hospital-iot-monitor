# Architecture

## System Overview

Hospital IoT Monitor is a three-layer system that simulates a production-grade healthcare sensor monitoring pipeline.

```
┌──────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  CLI / Bash  │  │  Log Files   │  │  Reports (txt)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  hospital_system.py   (Python Daemon)                │   │
│  │  • Sensor simulation engine                          │   │
│  │  • PID-based lifecycle management                    │   │
│  │  • Configurable thresholds                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Admin       │  │  Analysis    │  │  Archive         │  │
│  │  (Bash)      │  │  (Bash)      │  │  (Bash)          │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │  active_logs/    │  │  archived_logs/  │  │  reports/  │ │
│  │  chmod 700       │  │  chmod 700       │  │  chmod 700 │ │
│  └──────────────────┘  └──────────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Components

### 1. Sensor Daemon (`hospital_system.py`)

A background Python process that simulates IoT sensor data generation:

- **Heart Rate Monitors**: 5 ward sensors (WARD_A_HR_01–05)
  - Range: 45–150 BPM
  - Status: NORMAL, WARNING (90–100), CRITICAL (<60 or >100)
- **Temperature Sensors**: 5 ward sensors (WARD_B_TEMP_01–05)
  - Range: 34.5–40.5 °C
  - Status: NORMAL, CRITICAL (>38.0 or <35.5), WARNING (37.5–38.0)
- **Water Meters**: 2 facility meters (FACILITY_WATER_MAIN, ICU_WATER_RESERVE)
  - Range: 5–45 L/min
  - Status: NORMAL, HIGH_USAGE (>35)

The daemon forks into the background, writes a PID file to `/tmp/hospital_system.pid`, and logs sensor readings every second.

### 2. Admin Module (`hospital_admin.sh`)

Initialises the directory structure and applies mandatory access controls:

- Creates `active_logs/`, `archived_logs/`, `reports/`
- Sets directory permissions to `chmod 700` (owner-only access)
- Logs creation and permission events

### 3. Analysis Engine (`hospital_analysis.sh`)

Reads live log data and produces structured reports:

- Extracts CRITICAL events from heart rate and temperature logs
- Computes average ICU water consumption
- Writes timestamped reports to `reports/critical_alerts.txt`

### 4. Archive Module (`hospital_archive.sh`)

Manages log rotation to prevent unbounded disk usage:

- Moves active log files to `archived_logs/` with timestamp suffixes
- Creates fresh empty log files in `active_logs/`
- Preserves data lineage via `YYYYMMDD_HHMM` timestamps

## Data Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ GENERATE │───►│  SECURE  │───►│ MONITOR  │───►│  ANALYSE │───► REPORTS
│ (daemon) │    │ (admin)  │    │ (daemon) │    │ (bash)   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                    │
                                                    ▼
                                               ┌──────────┐
                                               │  ARCHIVE │───► archived_logs/
                                               │ (bash)   │
                                               └──────────┘
```

## Security Architecture

| Layer | Control | Rationale |
|-------|---------|-----------|
| Filesystem | `chmod 700` on log directories | Prevents unauthorised read access to PHI-simulated data |
| Filesystem | `chmod 600` on log files | Owner-only read/write for audit compliance |
| Processes | PID file in `/tmp` | Standard daemon lifecycle management |
| Container | Non-root `hospital` user | Principle of least privilege in Docker |

## Deployment Architecture

### Local

```bash
bash hospital_admin.sh        # Initialise + secure
python3 hospital_system.py start  # Start daemon
```

### Docker

```bash
docker build -t hospital-iot-monitor .
docker run -d --name hospital-iot hospital-iot-monitor
```

## Future Architecture

- **Ingestion Layer**: MQTT/HTTP API for real sensor data
- **Storage Layer**: Time-series database (InfluxDB/TimescaleDB)
- **Visualisation Layer**: Grafana dashboards
- **Alerting Layer**: Email/SMS/PagerDuty notifications
- **Compliance Layer**: HIPAA audit trail logging
