# Home Eye
This project serves web pages that display sensor values. Sensor values are fetched from [Home Store](http://github.com/johanlundahl/home_store).

This project is intended to use with [Home Monitor](http://github.com/johanlundahl/home_monitor), [Home Store](http://github.com/johanlundahl/home_store) and [Temp Sensor](http://github.com/johanlundahl/temp_sensor).

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

Set username and password that users can use to access the pages served by this application. Also set the secret key for the web app and the url to the data sources used by this app.

To enable HTTPS the application requires a cert and key file. See example on how to generate these files in [this blog post](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).


## Running

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
sudo reboot
```

## How to use the application
The web application is started on HTTPS on the port specified in the `home_eye/config.py` file. Required username and password is also defined in the config file.

Example:
```
https://localhost:5050
```