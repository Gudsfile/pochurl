FUNCTIONS_DIR=functions

functions-requirements:
	uv export --no-dev --locked --format requirements-txt --output-file $(FUNCTIONS_DIR)/requirements.txt

functions-venv:
	uv venv functions/venv --clear --seed
	cd $(FUNCTIONS_DIR) && . venv/bin/activate && pip install -r requirements.txt

emulators:
	GOOGLE_APPLICATION_CREDENTIALS="$(PWD)/${GOOGLE_APPLICATION_CREDENTIALS}" firebase emulators:start
