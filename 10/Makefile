SHELL := /bin/bash

all: create_activate_venv install_requirements setup_module

.PHONY: all, test

create_activate_venv:
	python3 -m venv venv

install_requirements:
	source venv/bin/activate; \
	pip3 install -r ../requirements.txt

setup_module:
	source venv/bin/activate; \
	python3 setup.py install

test:
	source venv/bin/activate; \
	pytest --disable-warnings

speed_check:
	source venv/bin/activate; \
	python compare_speed.py
