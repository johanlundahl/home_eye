
init:
	sudo pip3 install -r requirements.txt
	chmod +x home_eye/myapp.py

run:
	python3 -m home_eye.myapp

logging:
	tail -f application.log