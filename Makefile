
init:
	sudo pip3 install -r requirements.txt
	chmod +x home_eye/myapp.py

run:
	sudo python3 -m home_eye.myapp

update:
	git pull
	sudo pip3 install -r requirements.txt

logging:
	tail -f application.log