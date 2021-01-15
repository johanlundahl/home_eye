MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(dir $(MKFILE_PATH))

autostart:
	(crontab -l; echo "@reboot cd $(CURRENT_DIR) && python3 -m home_eye.myapp") | crontab -u pi -

init:
	sudo pip3 install -r requirements.txt
	chmod +x home_eye/myapp.py

logging:
	tail -f application.log

run:
	python3 -m home_eye.myapp

test:
	python3 -m unittest tests/*.py

update:
	git pull
	sudo pip3 install -r requirements.txt

apache-install:
	sudo apt update
	sudo apt install apache2
	sudo apt-get install libapache2-mod-wsgi-py3 python-dev

apache-logging:
	tail -f /var/log/apache2/error.log

apache-restart:
	sudo service apache2 restart

