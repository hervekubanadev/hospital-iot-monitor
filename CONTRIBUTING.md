# Contributing

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/hospital-iot-monitor.git
   cd hospital-iot-monitor
   ```

2. **Prerequisites**
   - Python 3.8+
   - Bash 4+
   - git

3. **Create a Python virtual environment** (optional)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Verify the setup**
   ```bash
   make test
   ```

## Coding Standards

### Python (`hospital_system.py`)
- Follow **PEP 8** with 4-space indentation.
- All functions **must** include type hints for parameters and return values.
- Use the `logging` module instead of `print` for daemon output.
- Use `pathlib.Path` for filesystem operations where practical.
- Handle `OSError` exceptions on all file I/O.
- Environment variables should be read at module level with `os.getenv()` and sensible defaults.

### Shell scripts (`hospital_*.sh`)
- Use **4-space indentation**.
- Quote all variable expansions (`"$var"`).
- Prefer `[[ ... ]]` over `[ ... ]` when using Bash.
- Use `local` for function-scoped variables where appropriate.
- Use `set -e` or explicit error handling.

### Git Commit Style
- Use [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat:` — new feature
  - `fix:` — bug fix
  - `refactor:` — code change that neither fixes a bug nor adds a feature
  - `docs:` — documentation only
  - `chore:` — tooling, config, or maintenance
- Keep commits focused on a single logical change.
- Write commit messages in the imperative mood: "Add signal handler" not "Added signal handler".

## Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. Make your changes in small, reviewable commits.

3. Ensure scripts are syntactically valid:
   ```bash
   python3 -m py_compile hospital_system.py
   bash -n hospital_*.sh
   ```

4. Run the test suite and confirm it passes:
   ```bash
   make test
   ```

5. Run the linter:
   ```bash
   make lint
   ```

6. Push your branch and open a pull request against `main`.

7. Your PR must be reviewed and approved by at least one maintainer before merging.

## Code of Conduct

All contributors are expected to be respectful and constructive. Harassment or abusive behaviour will not be tolerated.
