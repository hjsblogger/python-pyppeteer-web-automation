# Define variables
PYTHON := python3
PYTEST := pytest
PIP := pip3
PROJECT_NAME := web scraping using Python

.PHONY: install
install:
	$(PIP) install -r requirements.txt
	@echo "Set env vars LT_USERNAME & LT_ACCESS_KEY"
    # Procure Username and AccessKey from https://accounts.lambdatest.com/security
    export LT_USERNAME=himansh
    export LT_ACCESS_KEY=Ia1MiqNfci

.PHONY: install
poetry-install:
	poetry install

.PHONY: test
test:
    export NODE_ENV = test

.PHONY: test
pyunit-pyppeteer:
	- echo $(EXEC_PLATFORM)
	- $(PYTEST) --verbose --capture=no tests/pyunit/test_pyppeteer.py

.PHONY: test
pytest-pyppeteer:
	- echo $(EXEC_PLATFORM)
	- $(PYTEST) --verbose --capture=no tests/pytest/test_pyppeteer.py

# Currently being tested only on LambdaTest Cloud Grid
.PHONY: test
pytest-pyppeteer-parallel:
	- echo $(EXEC_PLATFORM)
	- $(PYTEST) --verbose --capture=no -n 4 tests/pytest/test_pyppeteer.py \
	tests/pytest/test_pyppeteer_2.py

###### Testing Headless - https://miyakogi.github.io/pyppeteer/reference.html#launcher 
.PHONY: test
pytest-pyppeteer-headless:
	- echo $(EXEC_PLATFORM)
	- echo $(BROWSER_MODE)
	- $(PYTEST) --verbose --capture=no tests/launcher/test_launcher_headless.py

###### Testing Custom Environment - https://miyakogi.github.io/pyppeteer/reference.html#environment-variables
# Available versions: 113, 121, and default 
.PHONY: test
pytest-pyppeteer-custom-exe:
	- echo $(EXEC_PLATFORM)
	- echo 'Browser Version:' $(CHROMIUM_VERSION)
	- $(PYTEST) --verbose --capture=no tests/launcher/test_launcher_exe_path.py

.PHONY: clean
clean:
    # This helped: https://gist.github.com/hbsdev/a17deea814bc10197285
	find . | grep -E "(__pycache__|\.pyc$$)" | xargs rm -rf
	@echo "Clean Succeded"

.PHONY: distclean
distclean: clean
	rm -rf venv

.PHONY: help
help:
	@echo ""
	@echo "install : Install project dependencies"
	@echo "clean : Clean up temp files"
	@echo "pytest-pyppeteer : Run Pyppeteer tests with Pytest framework"
	@echo "pyunit-pyppeteer : Run Pyppeteer tests with Pyunit framework"