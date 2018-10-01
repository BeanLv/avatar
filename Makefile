freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --output-file requirements.txt setup.py

install:
	pip install --no-cache -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

ut:
	APPCONFIG="tests/resources/config.app.yml" pytest tests/ut -svv

integration:
	APPCONFIG="tests/resources/config.app.yml" pytest tests/integration -svv