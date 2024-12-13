VENV_DIR = .venv

PYTHON = python3

$(VENV_DIR)/bin/activate: requirements.txt
		@echo "Creating virtual environment in $(VENV_DIR)..."
		$(PYTHON) -m venv $(VENV_DIR)
		@echo "Virtual environment created."
		@echo "Upgrading pip to the latest version..."
		$(VENV_DIR)/bin/python -m pip install --upgrade pip
		@echo "pip upgraded."
		@echo "Installing requirements..."
		$(VENV_DIR)/bin/pip install -r requirements.txt
		@echo "Requirements installed."

# Target to run the app.py script using the virtual environment
run: $(VENV_DIR)/bin/activate
		@echo "Running the server..."
		$(VENV_DIR)/bin/python app.py

# Default target to create the virtual environment
setup: $(VENV_DIR)/bin/activate

.PHONY: run setup
