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
	sudo python3 -m home_eye.myapp

update:
	git pull
	sudo pip3 install -r requirements.txt
