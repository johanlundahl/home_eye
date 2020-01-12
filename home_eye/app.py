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
    code_indoor, indoor_json = http.get_json('{}/api/sensors/indoor/latest'.format(config.sensors_url))
    sensors = [basement_json, outdoor_json, indoor_json]
    return render_template('home.html', sensors = sensors)

@app.route('/<name>', methods=['GET'])
@login_required
def sensor(name):
    code1, latest = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    code2, trend = http.get_json('{}/api/sensors/{}?size=30'.format(config.sensors_url, name))
    print('Fetching sensors', code1, len(latest), code2, len(trend))
    #code2, hourly_trend = http.get_json('{}/api/sensors/{}/hourly-trend'.format(config.sensors_url, name))
    #code2, daily_trend = http.get_json('{}/api/sensors/{}/daily-trend'.format(config.sensors_url, name))

    labels = [x['timestamp'] for x in trend]
    humidities = [x['humidity'] for x in trend]
    temperatures = [x['temperature'] for x in trend]

    return render_template('sensor.html', sensor = latest, active=['active', '', ''], chart_labels=labels, chart_humidity=humidities, chart_temperature=temperatures)

@app.route('/<name>/hours', methods=['GET'])
@login_required
def sensor_hours(name):
    code1, latest = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    code2, trend = http.get_json('{}/api/sensors/{}/hourly-trend'.format(config.sensors_url, name))
    
    labels = [x['timestamp'] for x in trend]
    humidities = [x['humidity'] for x in trend]
    temperatures = [x['temperature'] for x in trend]

    return render_template('sensor.html', sensor = latest, active=['', 'active', ''], chart_labels=labels, chart_humidity=humidities, chart_temperature=temperatures)

@app.route('/<name>/days', methods=['GET'])
@login_required
def sensor_days(name):
    code1, latest = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    code2, trend = http.get_json('{}/api/sensors/{}/daily-trend'.format(config.sensors_url, name))
    
    labels = [x['timestamp'] for x in trend]
    humidities = [x['humidity'] for x in trend]
    temperatures = [x['temperature'] for x in trend]

    return render_template('sensor.html', sensor = latest, active=['', '', 'active'], chart_labels=labels, chart_humidity=humidities, chart_temperature=temperatures)


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
        
