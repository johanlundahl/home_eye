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
$ sudo reboot
```

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

## Running with Apache

### Install Apache
This application can be served by a self hosted Apache web server. Follow [this tutorial](https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft) to set up the application to run under Apache. When run with Apache then `home_eye/myapp.wsgi` is the main application file.

Logging is then handled by Apache and the URL will be defined in the Apache configuration.

Start by [installing Apache to the Pi and configure the flask app](https://www.codementor.io/@abhishake/minimal-apache-configuration-for-deploying-a-flask-app-ubuntu-18-04-phu50a7ft). Start the Apache server with
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

```
<VirtualHost *:80>
     # Add machine's IP address (use ifconfig command)
     ServerName ip-address-of-host
     # Give an alias to to start your website url with
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

The following steps describe how to enable SSL for your application and is based on [a tutorial](https://hallard.me/enable-ssl-for-apache-server-in-5-minutes/).

Start by creating a ssl folder
```
$ sudo mkdir /etc/apache2/ssl
```

Generate self-signed certificate valid for 3 years (1095 days)
```
$ sudo openssl req -x509 -nodes -days 1095 -newkey rsa:2048 -out /etc/apache2/ssl/server.crt -keyout /etc/apache2/ssl/server.key
```

Enable the certificate
```
$ sudo a2enmod ssl
```

Edit the .conf file to include SSL

```
<VirtualHost *:443>
	SSLEngine On
	SSLCertificateFile /etc/ssl/certs/example.com.crt
	SSLCertificateKeyFile /etc/ssl/private/example.com.key
	...
```

To automatically redirect from http to https add the following to the VirtualHost for http
```
<VirtualHost *:80>
	...
	Redirect "/" "https://your_domain_or_IP/"
```

Restart apache for the changes to take affect
```
$ sudo service apache2 restart
```

<!--
TODO:
- dokumentera README för Apache
- config parameter för .wsgi filen


-->

