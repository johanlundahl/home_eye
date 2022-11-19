[![Lint](https://github.com/johanlundahl/home_eye/actions/workflows/python-app.yml/badge.svg)](https://github.com/johanlundahl/home_eye/actions/workflows/python-app.yml)
[![Test](https://github.com/johanlundahl/home_eye/actions/workflows/python-package.yml/badge.svg)](https://github.com/johanlundahl/home_eye/actions/workflows/python-package.yml)
[![Coverage](https://coveralls.io/repos/github/johanlundahl/home_eye/badge.svg?branch=master)](https://coveralls.io/github/johanlundahl/home_eye?branch=master)

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
$ make init
```

Edit myapp.yaml and add required configuration parameters for the application by
```
$ nano home_eye/myapp.yaml
```

Edit the `home_eye/myapp.yaml` to set the following configuration parameters:
```yaml
authentication:
    username: ''
    password: ''

web_server:
    port: 5050
    secret_key: ''

integration:
    sensors_url: ''
    solar_url: ''
    solar_api_key: ''
    app_root_path: ''
```

To enable HTTPS the application requires a cert and key file. See example on how to generate these files in [this blog post](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).


## Running

To start the application manually 
```
$ make run
```

To make the application start automatically at reboot run the following command
```
$ make autostart
```

Reboot your Rasperry Pi and the application will start:
```
$ sudo reboot
```

## Test
To run the tests for the application
```
$ make test
```

## Logging
Application events are logged to the application log file and can be viewed through
```
$ make logging
```


## How to use the application
The web application is started on HTTPS on the port specified in the `home_eye/config.py` file. Required username and password is also defined in the config file.

Example:
```
https://localhost:5050
```

## Running with Apache
This is a description on how to serve a flask application on a self hosted Apache web server on a Raspberry Pi running Raspbian.

### Install Apache
The following steps describe how to install Apache and is based on [this tutorial](https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft).

Install Apache
```
$ sudo apt update
$ sudo apt install apache2
```

Install mod_wsgi for python 3
```
$ sudo apt-get install libapache2-mod-wsgi-py3 python-dev
```

Start Apache
```
$ sudo service apache2 start
```

Check that the server in installed by visiting the Pi's IP in your browser.

### Configure Apache

Create a apache configuration file for your application 
```
$ sudo nano /etc/apache2/sites-available/example.conf
```
with the following content

```xml
<VirtualHost *:80>
     # Add machine's IP address (use ifconfig command)
     ServerName ip-address-of-host
     # Give an alias to to start your website url with
     WSGIDaemonProcess home_eye python-path=/home/pi/home_eye/:/usr/lib/python3/dist-packages/
     WSGIProcessGroup home_eye
     WSGIScriptAlias /home_eye /home/pi/home_eye/home_eye/myapp.wsgi
     <Directory /home/pi/home_eye/home_eye/>
            # set permissions as per apache2.conf file
            Options FollowSymLinks
            AllowOverride None
            Require all granted
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
<VirtualHost *:443>
     SSLEngine on
     # Add machine's IP address (use ifconfig command)
     ServerName test.jlundahl.com
     # Give an alias to to start your website url with
     WSGIDaemonProcess home_eye python-path=/home/pi/home_eye/:/usr/lib/python3/dist-packages/
     WSGIProcessGroup home_eye
     WSGIScriptAlias / /home/pi/home_eye/home_eye/myapp.wsgi

     <Directory /home/pi/home_eye/home_eye/>
            # set permissions as per apache2.conf file
            Options FollowSymLinks
            AllowOverride None
            Require all granted
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Enable the configuration
```
$ sudo a2ensite example.conf
```

Reload Apache configurations
```
$ sudo service apache2 start
```

Configure an A record with your domain pointing to your servers IP address. You'll find the IP address of your machine through `hostname -I`. The domain needs to be added in the application .conf file of Apache configuration in `/etc/apache/sites-available`.

### Enable SSL

Enable the certificate
```
$ sudo a2enmod ssl
```

Edit the .conf file to include SSL

```xml
<VirtualHost *:443>
    SSLEngine On
    ...
```

To automatically redirect from http to https add the following to the VirtualHost for http
```xml
<VirtualHost *:80>
    ...
    Redirect "/" "https://your_domain_or_IP/"
```
    
Use [Let's Encrypt](https://letsencrypt.org/getting-started/) to enable HTTPS on your local Apache installation. Follow the steps in [this tutorial](https://certbot.eff.org/lets-encrypt/pip-apache) to generate certificates with certbot.

Restart apache for the changes to take affect
```
$ sudo service apache2 restart
```

To view the web server error log enter
```
$ tail -f /var/log/apache2/error.log
```
