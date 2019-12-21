# home_eye

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

## Running

To start the application manually 
```
$ python3 -m home_eye.app
```

Make the python script executable:
```
$ chmod +x <python file>
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