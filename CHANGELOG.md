# Changelog

## [1.1.0] — 2026-06-30

### Refactor
- **Python daemon**: Replaced `os.fork()` with `subprocess.Popen` for better cross-platform compatibility. Added `logging` module in place of raw `print` statements. Introduced type hints on every function. Added `SIGTERM`/`SIGINT` handlers for graceful shutdown. All configuration values are now read from environment variables with sensible defaults. File write failures are caught and logged.

### Bug Fixes
- **Water usage audit** (`hospital_analysis.sh`): Corrected the `awk` field delimiter from `-F','` (comma) to `-F'|'` (pipe) to match the log format. Added whitespace trimming on the value field and appended the missing `L/min` unit to the output.
- **Log archive timestamp** (`hospital_archive.sh`): Removed the spurious space between `date +` and the format string, which caused a syntax error on some platforms.
- **Admin directory listing** (`hospital_admin.sh`): Fixed a copy-paste error where `archived_logs` appeared twice in the `ls` command instead of listing `active_logs` and `archived_logs`.
- **Unused variables** (`hospital_analysis.sh`): Removed three variables (`$1`, `$2`, `$3`) that were assigned but never referenced.

### Documentation
- Added `SECURITY.md` covering file permissions, PID file management, and log isolation.
- Added `CONTRIBUTING.md` with development setup, coding standards, and PR workflow.
- Added `CHANGELOG.md` for release history.

### Tooling
- Added `.editorconfig` for consistent indentation and line-ending settings across editors.
- Added `Makefile` with `start`, `stop`, `test`, `lint`, and `clean` targets.

## [1.0.0] — 2026-05-15

### Initial Release
- Hospital IoT sensor data simulation (heart rate, temperature, water usage).
- Bash-based admin, analysis, and archive scripts.
- Log rotation and critical alert reporting.
- Docker support with `Dockerfile`.
- GitHub Actions CI pipeline.
