install:
	sudo apt-get install python3 pip --upgrade
	python3 -m venv ./venv
	./venv/bin/pip install --upgrade Flask google-api-python-client google-auth-httplib2 google-auth-oauthlib

launch:
	./venv/bin/python3 -m flask --app script run
#--debug #--host=0.0.0.0