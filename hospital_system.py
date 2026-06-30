#!/usr/bin/env python3
import logging
import os
import random
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, NoReturn, Optional

LOG_DIR: str = os.getenv("LOG_DIR", "active_logs")
PID_FILE: str = os.getenv("PID_FILE", "/tmp/hospital_system.pid")
LOG_INTERVAL: int = int(os.getenv("LOG_INTERVAL_SECONDS", "1"))

HEART_RATE_MIN: int = int(os.getenv("HEART_RATE_MIN", "45"))
HEART_RATE_MAX: int = int(os.getenv("HEART_RATE_MAX", "150"))
TEMP_MIN: float = float(os.getenv("TEMP_MIN", "34.5"))
TEMP_MAX: float = float(os.getenv("TEMP_MAX", "40.5"))
WATER_USAGE_MIN: int = int(os.getenv("WATER_USAGE_MIN", "5"))
WATER_USAGE_MAX: int = int(os.getenv("WATER_USAGE_MAX", "45"))

CRITICAL_HR_LOW: int = int(os.getenv("CRITICAL_HR_LOW", "60"))
CRITICAL_HR_HIGH: int = int(os.getenv("CRITICAL_HR_HIGH", "100"))
CRITICAL_TEMP_HIGH: float = float(os.getenv("CRITICAL_TEMP_HIGH", "38.0"))
CRITICAL_TEMP_LOW: float = float(os.getenv("CRITICAL_TEMP_LOW", "35.5"))
WATER_HIGH_USAGE: int = int(os.getenv("WATER_HIGH_USAGE", "35"))

LOG_DIR_PERMISSIONS: int = int(os.getenv("LOG_DIR_PERMISSIONS", "700"), 8)
LOG_FILE_PERMISSIONS: int = int(os.getenv("LOG_FILE_PERMISSIONS", "600"), 8)

DEVICES: Dict[str, List[str]] = {
    "heart": [f"WARD_A_HR_{i:02d}" for i in range(1, 6)],
    "temp": [f"WARD_B_TEMP_{i:02d}" for i in range(1, 6)],
    "water": ["FACILITY_WATER_MAIN", "ICU_WATER_RESERVE"],
}

LOGS: Dict[str, str] = {
    "heart": os.path.join(LOG_DIR, "heart_rate_log.log"),
    "temp": os.path.join(LOG_DIR, "temperature_log.log"),
    "water": os.path.join(LOG_DIR, "water_usage_log.log"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("hospital_system")

_shutdown_requested: bool = False


def handle_signal(signum: int, frame) -> None:
    global _shutdown_requested
    _shutdown_requested = True
    logger.info("Received signal %s, shutting down gracefully...", signum)


def setup_signal_handlers() -> None:
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)


def ensure_environment() -> None:
    log_path = Path(LOG_DIR)
    log_path.mkdir(mode=LOG_DIR_PERMISSIONS, exist_ok=True)
    log_path.chmod(LOG_DIR_PERMISSIONS)

    headers: Dict[str, str] = {
        "heart": "Timestamp | Device_ID | Heart_Rate (BPM) | Status\n",
        "temp": "Timestamp | Device_ID | Temperature (Celsius) | Status\n",
        "water": "Timestamp | Device_ID | Usage (Liters/min) | Status\n",
    }

    for key, path in LOGS.items():
        p = Path(path)
        if not p.exists() or p.stat().st_size == 0:
            try:
                p.write_text(headers[key])
                p.chmod(LOG_FILE_PERMISSIONS)
            except OSError as exc:
                logger.error("Failed to write header to %s: %s", path, exc)
                raise


def _write_log(filepath: str, line: str) -> None:
    try:
        with open(filepath, "a") as f:
            f.write(line)
    except OSError as exc:
        logger.error("Failed to write to %s: %s", filepath, exc)


def generate_data() -> None:
    ensure_environment()
    setup_signal_handlers()

    while not _shutdown_requested:
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for device in DEVICES["heart"]:
            hr: int = random.randint(HEART_RATE_MIN, HEART_RATE_MAX)
            status: str = "NORMAL"
            if hr < CRITICAL_HR_LOW or hr > CRITICAL_HR_HIGH:
                status = "CRITICAL"
            elif CRITICAL_HR_HIGH - 10 <= hr <= CRITICAL_HR_HIGH:
                status = "WARNING"
            _write_log(LOGS["heart"], f"{timestamp} | {device} | {hr} | {status}\n")

        for device in DEVICES["temp"]:
            temp: float = round(random.uniform(TEMP_MIN, TEMP_MAX), 1)
            status = "NORMAL"
            if temp > CRITICAL_TEMP_HIGH:
                status = "CRITICAL"
            elif temp < CRITICAL_TEMP_LOW:
                status = "CRITICAL"
            elif CRITICAL_TEMP_HIGH - 0.5 <= temp <= CRITICAL_TEMP_HIGH:
                status = "WARNING"
            _write_log(LOGS["temp"], f"{timestamp} | {device} | {temp} | {status}\n")

        for device in DEVICES["water"]:
            usage: int = random.randint(WATER_USAGE_MIN, WATER_USAGE_MAX)
            status = "NORMAL"
            if usage > WATER_HIGH_USAGE:
                status = "HIGH_USAGE"
            _write_log(LOGS["water"], f"{timestamp} | {device} | {usage} | {status}\n")

        time.sleep(LOG_INTERVAL)


def start() -> None:
    pid: Optional[int] = _read_pid()
    if pid is not None and _is_process_running(pid):
        logger.warning("System is already running (PID %d).", pid)
        return

    try:
        proc = subprocess.Popen(
            [sys.executable, __file__, "run"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        _write_pid(proc.pid)
        logger.info("Hospital Management System started (PID: %d).", proc.pid)
    except OSError as exc:
        logger.error("Failed to start daemon: %s", exc)
        sys.exit(1)


def run() -> None:
    _write_pid(os.getpid())
    try:
        generate_data()
    finally:
        _remove_pid_file()


def stop() -> None:
    pid: Optional[int] = _read_pid()
    if pid is None:
        logger.info("No running system found.")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        logger.info("Hospital Management System stopped.")
    except ProcessLookupError:
        logger.info("No running system found (PID %d not found).", pid)
    finally:
        _remove_pid_file()


def _read_pid() -> Optional[int]:
    try:
        with open(PID_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError, OSError):
        return None


def _write_pid(pid: int) -> None:
    try:
        with open(PID_FILE, "w") as f:
            f.write(str(pid))
    except OSError as exc:
        logger.error("Failed to write PID file %s: %s", PID_FILE, exc)
        raise


def _remove_pid_file() -> None:
    try:
        os.remove(PID_FILE)
    except FileNotFoundError:
        pass
    except OSError as exc:
        logger.error("Failed to remove PID file %s: %s", PID_FILE, exc)


def _is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ./hospital_system.py [start|stop|run]")
        sys.exit(1)

    cmd: str = sys.argv[1].lower()
    if cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    elif cmd == "run":
        run()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
