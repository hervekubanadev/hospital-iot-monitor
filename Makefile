SHELL := /bin/bash
.PHONY: start stop test lint clean

start:
	./hospital_system.py start

stop:
	./hospital_system.py stop

test:
	@echo "Checking Python syntax..."
	python3 -m py_compile hospital_system.py
	@echo "Checking shell script syntax..."
	bash -n hospital_admin.sh
	bash -n hospital_analysis.sh
	bash -n hospital_archive.sh
	@echo "All syntax checks passed."

lint:
	@echo "Checking Python with pyflakes..."
	-python3 -m pyflakes hospital_system.py 2>/dev/null || true
	@echo "Checking shell scripts with shellcheck..."
	-shellcheck hospital_*.sh 2>/dev/null || true
	@echo "Lint checks complete."

clean:
	rm -rf active_logs archived_logs reports
	rm -f /tmp/hospital_system.pid
	@echo "Cleaned generated files and directories."
