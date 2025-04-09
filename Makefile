VENV_DIR = venv

setup: install run
reset: clean setup

# Install dependencies
install:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install requests ascii_magic flask pillow ansi2html

run:
	@$(VENV_DIR)/bin/python ascii.py

clean:
	@rm -rf $(VENV_DIR)
	@rm -rf uploads/*

