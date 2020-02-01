from flask import Flask, request, render_template ,redirect, url_for
from home_eye.flask_app import FlaskApp
from home_eye.model.user import User
from home_eye import config
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from pytils import http, logger
from OpenSSL import SSL
from datetime import datetime, timedelta
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
    
    code, overview = http.get_json('{}overview?api_key={}'.format(config.solar_url, config.solar_api_key))
    updated = overview['overview']['lastUpdateTime']
    current_power = float(overview['overview']['currentPower']['power']) #aktuell effekt i W
    day_energy = float(overview['overview']['lastDayData']['energy']) #kWh
    solar = [round(current_power), round(day_energy/1000), updated]
    return render_template('home.html', sensors = sensors, solar = solar)

@app.route('/favicon.ico', methods=['GET'])
@login_required
def favicon():
    return '', 200

@app.route('/<name>', methods=['GET'])
@login_required
def sensor(name):
    code1, latest = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    code2, trend = http.get_json('{}/api/sensors/{}?size=100'.format(config.sensors_url, name))
    trend = list(reversed(trend))

    labels = [x['timestamp'] for x in trend]
    humidities = [x['humidity'] for x in trend]
    temperatures = [x['temperature'] for x in trend]

    h_avg = round(sum(humidities)/len(humidities), 1)
    t_avg = round(sum(temperatures)/len(temperatures), 1)

    return render_template('sensor.html', sensor = latest, active=['active', '', ''], chart_labels=labels, chart_humidity=humidities, chart_temperature=temperatures, humidity_avg=h_avg, temperature_avg=t_avg)

@app.route('/<name>/hours', methods=['GET'])
@login_required
def sensor_hours(name):
    code1, latest = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    yesterday = datetime.now() - timedelta(days=1)
    code2, trend = http.get_json('{}/api/sensors/{}?timestamp[gt]={}&size=3600'.format(config.sensors_url, name, yesterday.strftime('%Y-%m-%d %H:%M:%S')))
    trend = trend[0::int(len(trend)/100)] if len(trend)>100 else trend
    trend = list(reversed(trend))

    labels = [x['timestamp'] for x in trend]
    humidities = [x['humidity'] for x in trend]
    temperatures = [x['temperature'] for x in trend]

    h_avg = round(sum(humidities)/len(humidities), 1)
    t_avg = round(sum(temperatures)/len(temperatures), 1)

    return render_template('sensor.html', sensor = latest, active=['', 'active', ''], chart_labels=labels, chart_humidity=humidities, chart_temperature=temperatures, humidity_avg=h_avg, temperature_avg=t_avg)

@app.route('/<name>/days', methods=['GET'])
@login_required
def sensor_days(name):
    code1, latest = http.get_json('{}/api/sensors/{}/latest'.format(config.sensors_url, name))
    code2, trend = http.get_json('{}/api/sensors/{}/daily-trend'.format(config.sensors_url, name))
    trend = list(reversed(trend))

    labels = [x['timestamp'] for x in trend]
    humidities = [x['humidity'] for x in trend]
    temperatures = [x['temperature'] for x in trend]

    h_avg = round(sum(humidities)/len(humidities), 1)
    t_avg = round(sum(temperatures)/len(temperatures), 1)

    return render_template('sensor.html', sensor = latest, active=['', '', 'active'], chart_labels=labels, chart_humidity=humidities, chart_temperature=temperatures, humidity_avg=h_avg, temperature_avg=t_avg)


@app.route('/solar', methods=['GET'])
@login_required
def solar():
    url = '{}overview?api_key={}'.format(config.solar_url, config.solar_api_key)
    code, overview = http.get_json(url)

    solar = {}
    solar['energy'] = round(overview['overview']['lastDayData']['energy']/1000)
    solar['power'] = round(overview['overview']['currentPower']['power']/1000)
    solar['timestamp'] = overview['overview']['lastUpdateTime']

    return render_template('solar.html', sensor=solar)

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
        
