<div align="center">
  <h1>Hospital IoT Monitor</h1>
  <p><strong>Real-time sensor monitoring infrastructure for healthcare facilities</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3-3776AB" alt="Python 3">
    <img src="https://img.shields.io/badge/Bash-4EAA25" alt="Bash">
    <img src="https://img.shields.io/badge/IoT_Simulation-00B4AB" alt="IoT Simulation">
    <img src="https://img.shields.io/badge/Healthcare_Tech-FF6B6B" alt="Healthcare">
  </p>
</div>

---

## Overview

A hospital IoT sensor monitoring system that simulates a real-time infrastructure for healthcare facilities. It generates synthetic sensor data (heart rate, body temperature, water usage), enforces data security through Linux permissions, performs automated analysis for critical alerts, and manages log rotation — mimicking a production hospital monitoring pipeline.

Designed as an educational prototype demonstrating the intersection of healthcare technology, IoT simulation, and systems administration.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Python Daemon (hospital_system.py)       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Heart Rate   │  │ Temperature  │  │ Water Usage  │   │
│  │ 5 Sensors    │  │ 5 Sensors    │  │ 2 Meters     │   │
│  │ 45-150 BPM   │  │ 34.5-40.5°C  │  │ 5-45 L/min   │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         └─────────────────┴─────────────────┘            │
│                           │                              │
│                    Writes every 1 second                  │
└───────────────────────────┬──────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
  heart_rate_log.log  temperature_log.log  water_usage_log.log
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
    ┌─────────▼────────┐       ┌─────────▼────────┐
    │ hospital_admin.sh │       │ hospital_analysis │
    │ - Directory setup │       │   .sh             │
    │ - Permissions     │       │ - Critical alerts │
    │ - Security (600)  │       │ - Water audit     │
    └───────────────────┘       └─────────┬─────────┘
                                          │
                                ┌─────────▼────────┐
                                │ hospital_archive  │
                                │   .sh             │
                                │ - Log rotation    │
                                │ - Timestamped     │
                                │   archiving       │
                                └───────────────────┘
```

---

## Features

### 🔬 Sensor Simulation (Python Daemon)
- **Heart Rate Monitoring:** 5 ward sensors (45-150 BPM) with CRITICAL/WARNING/NORMAL status
- **Body Temperature:** 5 ward sensors (34.5-40.5°C) with configurable thresholds
- **Water Usage:** 2 facility meters (5-45 L/min) with HIGH_USAGE detection
- Background daemon with PID-based lifecycle management

### 🔒 Data Security (System Administration)
- Automatic directory structure creation
- Linux file permission hardening (`chmod 600`)
- Secure log file isolation

### 📊 Automated Analysis
- CRITICAL alert extraction from vital signs
- ICU water consumption auditing
- Timestamped report generation

### 📦 Log Management
- Automated log rotation with timestamped archives
- Fresh log file recreation after rotation
- Archive directory organization

---

## Quick Start

### Prerequisites
- Python 3
- Bash shell (Linux/macOS)
- Standard Unix utilities (`grep`, `awk`, `date`, `tar`)

### Running the System

```bash
# 1. Initialize the monitoring environment
bash hospital_admin.sh

# 2. Start the sensor data generator daemon
python3 hospital_system.py start

# 3. Run analysis on collected data
bash hospital_analysis.sh

# 4. Archive old logs (when ready)
bash hospital_archive.sh

# 5. Stop the daemon when done
python3 hospital_system.py stop
```

### Data Flow

```
Generate → Secure → Monitor → Analyze → Archive
  (daemon)  (admin)  (real-time)  (reports)  (rotation)
```

---

## Project Structure

```
├── hospital_system.py       # Python daemon - sensor data generation
├── hospital_admin.sh        # System initialization & security setup
├── hospital_analysis.sh     # Automated alert analysis & reporting
├── hospital_archive.sh      # Log rotation & archiving
├── active_logs/             # Live sensor data directory (600 permissions)
├── archived_logs/           # Rotated log archive directory
└── reports/                 # Analysis output directory
```

### Generated Data Format

Each sensor writes one record per second:

```
2026-06-30 14:30:01 | WARD_A_HR_01 | 72 | NORMAL
2026-06-30 14:30:01 | WARD_B_TEMP_03 | 38.2 | CRITICAL
2026-06-30 14:30:01 | ICU_WATER_RESERVE | 28 | NORMAL
```

---

## Roadmap

- [x] Multi-sensor data generation (heart rate, temperature, water)
- [x] Background daemon with PID lifecycle
- [x] Automated critical alert detection
- [x] Secure log management with permissions
- [x] Log rotation and archiving
- [ ] Real-time dashboard (Grafana integration)
- [ ] Alert notifications (email/SMS)
- [ ] Historical trend analysis
- [ ] Patient record correlation
- [ ] HIPAA compliance documentation
- [ ] Docker containerization
- [ ] MQTT/HTTP API for sensor data ingestion

---

## Use Cases

- **Healthcare IT Education:** Learn how IoT monitoring infrastructure operates in hospital settings
- **Systems Administration Practice:** Hands-on with daemon management, permissions, and log rotation
- **IoT Prototyping:** Template for building real sensor monitoring pipelines
- **DevOps Training:** Infrastructure-as-code approach to healthcare monitoring

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Contact

**KUBANA Friend Herve** - [hervekubana.dev](https://hervekubana.dev)

Project Link: [https://github.com/hervekubanadev/hospital-iot-monitor](https://github.com/hervekubanadev/hospital-iot-monitor)

---

<div align="center">
  <sub>Built with ❤️ for healthcare technology education | Kigali, Rwanda</sub>
</div>
