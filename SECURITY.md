# Security Policy

## File Permissions

The system applies strict file and directory permissions to protect sensitive hospital data.

| Resource            | Permission | Owner |
|---------------------|------------|-------|
| `active_logs/`      | 700        | User  |
| `*.log` files       | 600        | User  |
| PID file            | 644        | User  |
| Shell scripts       | 755        | User  |
| Python modules      | 755        | User  |

- **Log directories** (`active_logs/`, `archived_logs/`, `reports/`): Mode `700` — only the owner may read, write, or traverse them.
- **Log files**: Mode `600` — owner-only read/write. No group or world access.
- **Executable scripts** (`hospital_*.sh`, `hospital_system.py`): Mode `755` — readable and executable by all, writable only by owner.
- Permissions are applied at creation time via `os.getenv("LOG_DIR_PERMISSIONS", "700")` and `os.getenv("LOG_FILE_PERMISSIONS", "600")`, parsed as octal values.

## PID File Management

The PID file (`/tmp/hospital_system.pid`) tracks the daemon process:

- Written atomically at daemon start.
- Removed on clean shutdown via `SIGTERM`/`SIGINT`.
- Guarded against stale PID files: `start()` checks whether the recorded PID is still alive with `os.kill(pid, 0)` before attempting to start a new instance.
- PID file read/write failures are logged and escalated to the caller.
- The file path is configurable via the `PID_FILE` environment variable.

## Log Isolation

- Each sensor category (heart rate, temperature, water usage) writes to a separate log file under `active_logs/`.
- Log files are appended to — never overwritten in normal operation.
- Log archiving moves files to `archived_logs/` with a timestamp suffix and recreates empty originals.
- Header rows are written once per file; subsequent data rows use the same pipe-delimited format.
- No PII or PHI is stored in logs. All device identifiers are synthetic.

## Environment Variables

Sensitive or environment-specific values are supplied through environment variables (not hard-coded):

- `LOG_DIR`, `PID_FILE` — path configuration
- `LOG_DIR_PERMISSIONS`, `LOG_FILE_PERMISSIONS` — octal permission masks
- `HEART_RATE_MIN`/`MAX`, `TEMP_MIN`/`MAX`, `WATER_USAGE_MIN`/`MAX` — simulation ranges
- `CRITICAL_HR_LOW`/`HIGH`, `CRITICAL_TEMP_LOW`/`HIGH`, `WATER_HIGH_USAGE` — alert thresholds

A `.env.example` file documents all variables with safe defaults. Production deployments should copy this to `.env` and adjust values as needed.

## Reporting Vulnerabilities

Report security issues by opening a GitHub Issue. Do not disclose sensitive findings publicly until a fix has been released.
