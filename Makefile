# Define the Python command
PYTHON = python3

# Define the name of the package
PACKAGE = software-properties-station

# Define where your setup.py is located if it exists
SETUP_PY = setup.py

# Define the log file path
LOG_FILE = /var/log/$(PACKAGE).log

# Path to your virtual environment
VENV_PATH = .venv

# Default target
all: install

# Create virtual environment
$(VENV_PATH):
	@echo "Creating virtual environment"
	$(PYTHON) -m venv $(VENV_PATH)

# Install target, uses virtual environment and then copies the binary to system-wide location
install: $(VENV_PATH) create_log
	@echo "Activating virtual environment"
	@. $(VENV_PATH)/bin/activate; \
	$(PYTHON) -m pip install --upgrade --force-reinstall .
	@echo "Copying binary to /usr/local/bin"
	@if [ -f "$(VENV_PATH)/bin/$(PACKAGE)" ]; then \
	    sudo cp $(VENV_PATH)/bin/$(PACKAGE) /usr/local/bin/; \
	else \
	    echo "Error: Binary $(PACKAGE) not found in $(VENV_PATH)/bin/"; \
	    exit 1; \
	fi

# Create log file and set permissions
create_log:
	@echo "Creating log file $(LOG_FILE)"
	@sudo touch $(LOG_FILE)
	@sudo chown root:$(shell id -gn) $(LOG_FILE)
	@sudo chmod 640 $(LOG_FILE)

# Uninstall target, uses virtual environment for clean removal
uninstall: $(VENV_PATH)
	@echo "Uninstalling all versions of $(PACKAGE) from virtual environment"
	@. $(VENV_PATH)/bin/activate; \
	$(PYTHON) -m pip uninstall -y $(PACKAGE) || true
	@echo "Removing binary from /usr/local/bin"
	@sudo rm -f /usr/local/bin/$(PACKAGE)
	@echo "Removing log file $(LOG_FILE)"
	@sudo rm -f $(LOG_FILE)

# Clean target to remove build artifacts and virtual environment if needed
clean:
	rm -rf build dist *.egg-info

# Target to remove virtual environment
clean-venv:
	rm -rf $(VENV_PATH)

# Test target, uses virtual environment
test: $(VENV_PATH)
	@echo "Running tests in virtual environment"
	@. $(VENV_PATH)/bin/activate; \
	$(PYTHON) -m unittest discover tests

# Phony targets
.PHONY: all install uninstall clean clean-venv test create_log
