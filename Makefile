VENV 	= venv
PYTHON 	= $(VENV)/bin/python
reload:pre-reload
	sudo supervisorctl status gunlog | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs kill -HUP

pre-reload:
	echo Hello

test-run-fastapi:
	$(PYTHON) -m uvicorn backend.http.main:app --port 8450

install:
	$(PYTHON) -m pip install -r requirements.txt

