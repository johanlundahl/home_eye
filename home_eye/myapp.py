from datetime import datetime, timedelta
import os
from box import Box
from flask import Flask, request, render_template ,redirect, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import yaml
from pytils import http
import pytils.log as logz
from pytils.date import Date, Week, Month, Year
from pytils import config
from pytils.http import Navigation
from home_eye.flask_app import FlaskApp
from home_eye.model.user import User
from home_eye.service.solar_proxy import SolarProxy, TimeUnit
from home_eye.model.sensor_proxy import SensorProxy

# load config from file
here = os.path.dirname(__file__)
cfg_file = os.path.join(here, 'myapp.yaml')
cfg = config.init(cfg_file) 

app = FlaskApp(__name__)
app.secret_key = cfg.web_server.secret_key
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

solar_proxy = SolarProxy(cfg.integration.solar_url, cfg.integration.solar_api_key)
sensor_proxy = SensorProxy(cfg.integration.sensors_url)

@login_manager.user_loader
def load_user(user_id):
    return User('', '')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST' and has_login_parameters(request):
        username = request.form['username']
        password = request.form['password']
        
        if username == cfg.authentication.username and password == cfg.authentication.password:
            login_user(User(username, password))
            
        return redirect(url_for('home'))
    return 500

def has_login_parameters(request):
    return all(x in request.form for x in ['username', 'password'])

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/favicon.ico', methods=['GET'])
@login_required
def favicon():
    return '', 200

@app.route('/', methods=['GET'])
@login_required
def home():
    solar = solar_proxy.get_today()
    sensors = ['basement', 'outdoor', 'indoor']    
    return render_template('home.html', sensors = sensors, solar = solar)

@app.route('/api/v2/sensors/<name>/latest', methods=['GET'])
@login_required
def sensor_latest(name):
    sensor = sensor_proxy.get_latest(name)
    return jsonify(sensor.to_json())

@app.route('/v2/<name>/latest', methods=['GET'])
@login_required
def v2_sensor(name):
    date = datetime.now().strftime('%Y-%m-%d')
    latest = sensor_proxy.get_latest(name)
    min_max = sensor_proxy.get_min_max(name, date)
    return render_template('sensor-latest.html', sensor = latest, min_max = min_max)

@app.route('/v2/<name>/day', methods=['GET'])
@login_required
def v2_sensor_day(name):
    date = Date.parse(request.args['date']) if 'date' in request.args else Date.current()
    history = sensor_proxy.get_day(name, day=str(date))
    link = '/v2/{}/day?date={}'
    prev_link = link.format(name, str(date.prev))
    next_link = link.format(name, str(date.next))
    nav = Navigation(str(date), prev_link, next_link)
    return render_template('sensor-history.html', name=name, nav=nav, active=['active', '', '', ''], history=history)

@app.route('/v2/<name>/week', methods=['GET'])
@login_required
@http.validate_querystrings(method='GET', parameters=['date'])
def v2_sensor_week(name):
    a_date = request.args['date'] if 'date' in request.args else str(Date.current())

    week = Week.create(Date.parse(a_date))
    
    monday, sunday = week.range()
    history = sensor_proxy.get_days(name, first=monday, last=sunday)
    link = '/v2/{}/week?date={}'
    prev_link = link.format(name, week.prev().range()[0])
    next_link = link.format(name, week.next().range()[0])
    nav = Navigation(week.name, prev_link, next_link)
    return render_template('sensor-history.html', name=name, nav=nav, active=['', 'active', '', ''], history=history)

@app.route('/v2/<name>/month', methods=['GET'])
@login_required
def v2_sensor_month(name):
    first = Date.parse(request.args['from']) if 'from' in request.args else Month.current().range()[0]
    last = Date.parse(request.args['to']) if 'to' in request.args else Month.current().range()[1]
    history = sensor_proxy.get_days(name, first=first, last=last)
    
    link = '/v2/{}/month?from={}&to={}'
    month = Month.create(first)
    prev_link = link.format(name, *month.prev().range())
    next_link = link.format(name, *month.next().range())
    nav = Navigation(month.name, prev_link, next_link)
    return render_template('sensor-history.html', name=name, nav=nav, active=['', '', 'active', ''], history=history)

@app.route('/v2/energy/production/today', methods=['GET'])
@login_required
def solar_today():
    solar = solar_proxy.get_today()
    solar_history = solar_proxy.get_energy_latest(days=7)
    return render_template('solar-latest.html', solar=solar, history=solar_history)

@app.route('/v2/energy/production/month', methods=['GET'])
@login_required
def solar_month():
    first = Date.parse(request.args['from']) if 'from' in request.args else Month.current().range()[0]
    last = Date.parse(request.args['to']) if 'to' in request.args else Month.current().range()[1]
    
    solar_history = solar_proxy.get_energy_history(first.name, last.name)
    solar_history.dates = [Date.parse(x).datetime.day for x in solar_history.dates]
    
    link = '/v2/energy/production/month?from={}&to={}'
    month = Month.create(first)
    prev_link = link.format(*month.prev().range())
    next_link = link.format(*month.next().range())
    nav = Navigation(month.name, prev_link, next_link)
    return render_template('solar-history.html', history=solar_history, nav=nav)

@app.route('/v2/energy/production/year', methods=['GET'])
@login_required
def solar_year():
    year = Year.current()
    first = Date.parse(request.args['from']) if 'from' in request.args else year.range()[0]
    last = Date.parse(request.args['to']) if 'to' in request.args else year.range()[1]
   
    solar_history = solar_proxy.get_energy_history(first.name, last.name, time_unit=TimeUnit.MONTH)
    solar_history.dates = [Date.parse(x).datetime.month for x in solar_history.dates]
    
    link = '/v2/energy/production/year?from={}&to={}'
    year = Year.create(first)
    prev_link = link.format(*year.prev().range())
    next_link = link.format(*year.next().range())
    nav = Navigation(year.name, prev_link, next_link)
    return render_template('solar-history.html', history=solar_history, nav=nav)


@app.route('/application/logs', methods=['GET'])
@login_required
def application_logs():
    with open('{}/application.log'.format(cfg.application.app_root_path), 'r') as log:
        log_lines = log.readlines()
        return render_template('application-log.html', log_lines=log_lines)

@app.route('/application/storage', methods=['GET'])
@login_required
def storage():
    status = sensor_proxy.get_status()
    return render_template('storage.html', status = status)


if __name__ == '__main__':
    try:
        logz.init()
        app.run(host='0.0.0.0', port=cfg.web_server.port)
    except Exception:
        logz.exception('Application Exception')
        
