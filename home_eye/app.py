from flask import Flask, request, render_template ,redirect, url_for
from home_eye.flask_app import FlaskApp
from home_eye.model.user import User
from home_eye import config
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from pytils import http, logger
from OpenSSL import SSL
import os
import sys

app = FlaskApp(__name__)
app.secret_key = config.app_secret_key
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # load user from db    
    return User('', '')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST' and all(x in request.form for x in ['username', 'password']):
        username = request.form['username']
        password = request.form['password']
        
        if username == config.username and password == config.password:
            login_user(User(username, password))
            
        return redirect(url_for('home'))
    return 500

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/', methods=['GET'])
@login_required
def home():
    code_basement, basement_json = http.get_json('{}/api/sensors/basement/latest'.format(config.sensors_url))
    code_outdoor, outdoor_json = http.get_json('{}/api/sensors/outdoor/latest'.format(config.sensors_url))
    sensors = [basement_json, outdoor_json]
    return render_template('home.html', sensors = sensors, basement = basement_json, outdoor = outdoor_json)

@app.route('/<name>', methods=['GET'])
@login_required
def sensor(name):
    code1, json = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    code2, hourly_trend = http.get_json('{}/api/sensors/{}/hourly-trend'.format(config.sensors_url, name))
    code2, daily_trend = http.get_json('{}/api/sensors/{}/daily-trend'.format(config.sensors_url, name))

    labels = [x['timestamp'] for x in hourly_trend]
    humidity_data = [x['humidity'] for x in hourly_trend]
    temperature_data = [x['temperature'] for x in hourly_trend]


    
    return render_template('sensor.html', sensor = json, labels = labels, humidity = humidity_data, temperature = temperature_data, daily_trend = daily_trend)


if __name__ == '__main__':
    if 'win32' in sys.platform:
        app.run(host='0.0.0.0')
    else:
        try:
            logger.init()
            context = SSL.Context(SSL.SSLv23_METHOD)
            crt = os.path.join(os.path.dirname(__file__), config.crt_file)
            key = os.path.join(os.path.dirname(__file__), config.key_file)
            context = (crt, key)
            app.run(host='0.0.0.0', port=config.app_port, ssl_context='adhoc')
        except Exception:
            logger.exception('Application Exception')
        
