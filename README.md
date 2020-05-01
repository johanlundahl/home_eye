# Home Eye
This project serves web pages that display sensor values. Sensor values are fetched from [Home Store](http://github.com/johanlundahl/home_store).

This project is suitable to run on a Raspberry Pi and is intended to use with [Home Monitor](http://github.com/johanlundahl/home_monitor), [Home Store](http://github.com/johanlundahl/home_store), [Temp Sensor](http://github.com/johanlundahl/temp_sensor) and [Mosquitto MQTT Broker](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/).

## Installation

Clone this git repo

```
$ git clone https://github.com/johanlundahl/home_eye
```

Install required python modules

```
$ sudo pip3 install -r requirements.txt
```

Edit config.py and add required configuration parameters for the application by
```
$ nano home_eye/config.py
```

Edit the `home_eye/config.py` to set the following configuration parameters:
```
username = 'username-to-this-web-application'
password = 'password-to-this-web-application'
app_secret_key = 'secrec-key-used-by-web-server'
app_port = 5050		# port exposing this web application on
sensors_url = 'http://base-url-to-home-store'
crt_file = 'cert-file-name'
key_file = 'key-file-name'
```

To enable HTTPS the application requires a cert and key file. See example on how to generate these files in [this blog post](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).


## Running standalone

To start the application manually 
```
$ python3 -m home_eye.app
```

Make the python script executable:
```
$ chmod +x home_eye/app.py
```

To make the application start automatically define a crontab job. Edit crontab by
```
$ crontab -e
```

Define which time the different jobs should be run at, e.g.
```
@reboot python3 /home/pi/home_eye/home_eye/app.py
```

Reboot your Rasperry Pi and the application will start:
```
$ sudo reboot
```

## Running with Apache

Follow [this tutorial](https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft) to set up the application to run under Apache. When run with Apache then `home_eye/myapp.wsgi` is the main application file.

## Logging
Application events are logged to the application log file and can be viewed through
```
$ tail -f application.log
```


## How to use the application
The web application is started on HTTPS on the port specified in the `home_eye/config.py` file. Required username and password is also defined in the config file.

Example:
```
https://localhost:5050
```