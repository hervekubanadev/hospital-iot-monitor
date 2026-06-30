<div align="center">
  <h1>Hospital IoT Monitor</h1>
  <p><strong>AI-Assisted Healthcare Operations Monitoring Infrastructure</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3-3776AB" alt="Python 3">
    <img src="https://img.shields.io/badge/Bash-4EAA25" alt="Bash">
    <img src="https://img.shields.io/badge/IoT_Simulation-00B4AB" alt="IoT Simulation">
    <img src="https://img.shields.io/badge/Healthcare_Tech-FF6B6B" alt="Healthcare">
    <img src="https://img.shields.io/badge/Docker-2496ED" alt="Docker">
  </p>
</div>

---

## Problem Statement

Healthcare facilities in emerging markets lack affordable, real-time monitoring infrastructure for critical patient vitals and facility operations. Manual charting introduces latency, human error, and data gaps that compromise patient safety. Hospital IoT Monitor addresses this by providing a zero-cost simulation and monitoring framework that demonstrates how AI-assisted sensor pipelines can transform healthcare operations — from vital-sign tracking to water resource management — while enforcing security controls compliant with healthcare data protection standards.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                            │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │  CLI / Bash    │  │  Log Files      │  │  Reports         │  │
│  └────────────────┘  └─────────────────┘  └──────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                     APPLICATION LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  hospital_system.py   —  Python Sensor Daemon            │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │   │
│  │  │ Heart Rate │  │Temperature │  │  Water Usage     │   │   │
│  │  │ 5 Sensors  │  │ 5 Sensors  │  │  2 Meters        │   │   │
│  │  │ 45-150 BPM │  │34.5-40.5°C │  │  5-45 L/min      │   │   │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Admin       │  │  Analysis    │  │  Archive             │  │
│  │  (Bash)      │  │  (Bash)      │  │  (Bash)              │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                       DATA LAYER                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │  active_logs/    │  │  archived_logs/  │  │  reports/      │ │
│  │  chmod 700       │  │  chmod 700       │  │  chmod 700     │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
└──────────────────────────────────────────────────────────────────┘

                         Data Flow
  Generate ──► Secure ──► Monitor ──► Analyse ──► Archive
  (daemon)    (admin)    (real-time)  (reports)   (rotation)
```

---

## Features

### AI-Assisted Sensor Simulation
- **Heart Rate Monitoring**: 5 ward sensors (45-150 BPM) with intelligent status classification (NORMAL/WARNING/CRITICAL)
- **Body Temperature**: 5 ward sensors (34.5-40.5°C) with hypothermia and fever detection
- **Water Usage**: 2 facility meters (5-45 L/min) with HIGH_USAGE anomaly detection
- Background daemon with PID-based lifecycle management

### Security & Compliance
- Linux file permission hardening (`chmod 700` on directories, `chmod 600` on files)
- Non-root container execution (principle of least privilege)
- Audit trail via timestamped log rotation
- HIPAA-aligned data access controls

### Automated Operations
- CRITICAL alert extraction from vital signs
- ICU water consumption auditing
- Timestamped report generation
- Automated log rotation with data lineage preservation

### Deployment Flexibility
- Bare-metal Linux/macOS deployment
- Docker containerisation with multi-stage builds
- Configurable via environment variables

---

## Security

This system enforces mandatory access controls at the filesystem level to protect sensitive healthcare data:

| Control | Scope | Mechanism |
|---------|-------|-----------|
| Directory isolation | `active_logs/` | `chmod 700` — owner-only access |
| File hardening | Log files | `chmod 600` — owner-only read/write |
| Process isolation | Daemon | PID file in `/tmp` with SIGTERM lifecycle |
| Container security | Docker | Non-root `hospital` user |

Run `bash hospital_admin.sh` to apply all security controls before starting the daemon.

---

## Quick Start

### Prerequisites
- Python 3
- Bash shell (Linux/macOS)
- Docker (optional)

### Local Deployment

```bash
# 1. Clone the repository
git clone https://github.com/hervekubanadev/hospital-iot-monitor.git
cd hospital-iot-monitor

# 2. Copy environment configuration
cp .env.example .env

# 3. Initialise and secure the monitoring environment
bash hospital_admin.sh

# 4. Start the sensor data generator daemon
python3 hospital_system.py start

# 5. Run analysis on collected data
bash hospital_analysis.sh

# 6. Archive old logs
bash hospital_archive.sh

# 7. Stop the daemon
python3 hospital_system.py stop
```

### Docker Deployment

```bash
# Build the image
docker build -t hospital-iot-monitor .

# Run in background
docker run -d --name hospital-iot \
  -v $(pwd)/active_logs:/app/active_logs \
  -v $(pwd)/archived_logs:/app/archived_logs \
  -v $(pwd)/reports:/app/reports \
  hospital-iot-monitor
```

---

## Project Structure

```
├── hospital_system.py       # Python daemon — sensor data generation
├── hospital_admin.sh        # System initialisation & security setup
├── hospital_analysis.sh     # Automated alert analysis & reporting
├── hospital_archive.sh      # Log rotation & archiving
├── Dockerfile               # Multi-stage container build
├── .env.example             # Environment variable template
├── .gitignore               # Ignored files and directories
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline (ShellCheck + Python lint/test)
├── docs/
│   ├── ARCHITECTURE.md      # Detailed system architecture
│   └── API.md               # Command and data format reference
├── active_logs/             # Live sensor data directory (700 permissions)
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
- [x] Secure log management with Linux permissions
- [x] Log rotation and archiving
- [x] Docker containerisation
- [ ] Real-time dashboard (Grafana integration)
- [ ] Alert notifications (email/SMS/PagerDuty)
- [ ] Historical trend analysis with ML anomaly detection
- [ ] Patient record correlation engine
- [ ] HIPAA compliance documentation
- [ ] MQTT/HTTP API for real sensor data ingestion
- [ ] Time-series database integration (InfluxDB)
- [ ] Web-based monitoring dashboard

---

## Use Cases

- **Healthcare IT Education**: Understand how IoT monitoring infrastructure operates in hospital settings
- **Systems Administration Practice**: Hands-on with daemon management, permissions, and log rotation
- **IoT Prototyping**: Template for building production sensor monitoring pipelines
- **DevOps Training**: Infrastructure-as-code approach to healthcare monitoring
- **Compliance Demonstration**: Reference architecture for healthcare data protection

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Contact

**KUBANA Friend Herve** — [hervekubana.dev](https://hervekubana.dev)

Project Link: [https://github.com/hervekubanadev/hospital-iot-monitor](https://github.com/hervekubanadev/hospital-iot-monitor)

---

<div align="center">
  <sub>Built with ❤️ for healthcare technology innovation | Kigali, Rwanda</sub>
</div>
