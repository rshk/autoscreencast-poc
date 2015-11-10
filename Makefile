.PHONY: all clean setup virtualenv requirements

VENV_PATH = venv

all:
	mkdir output tmp
	xvfb-run -s '-screen 0 1920x1200x24' $(VENV_PATH)/bin/python ./bin/build.py

clean:
	rm -rf output tmp

setup: virtualenv

virtualenv:
	virtualenv --python /usr/bin/python2.7 $(VENV_PATH)
	$(VENV_PATH)/bin/pip install pip-tools
	$(VENV_PATH)/bin/pip-sync requirements.txt

requirements: requirements.txt

requirements.txt: requirements.in
	pip-compile requirements.in
