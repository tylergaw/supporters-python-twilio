.PHONY: run setup

setup:
	python setup.py develop

run:
	python supporters_twilio/application.py
