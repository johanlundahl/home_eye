from datetime import datetime, timedelta
import os
from box import Box
from flask import Flask, request, render_template ,redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import yaml
from pytils import http
import pytils.log as logz
from pytils.date import Date, Week
from pytils import config
from pytils import config
from pytils.http import Navigation
from home_eye.flask_app import FlaskApp
from home_eye.model.user import User
from home_eye.model.solar_proxy import SolarProxy
from home_eye.model.sensor_proxy import SensorProxy

here = os.path.dirname(__file__)
cfg_file = os.path.join(here, 'myapp.yaml')
print(cfg_file)
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
    basement = sensor_proxy.get_latest('basement')
    outdoor = sensor_proxy.get_latest('outdoor')
    indoor = sensor_proxy.get_latest('indoor')
    sensors = [basement, outdoor, indoor]    
    solar = solar_proxy.get_today()

    return render_template('home.html', sensors = sensors, solar = solar)

@app.route('/storage', methods=['GET'])
@login_required
def storage():
    status = sensor_proxy.get_status()
    return render_template('storage.html', status = status)


@app.route('/<name>', methods=['GET'])
@login_required
def sensor(name):
    latest = sensor_proxy.get_latest(name)
    history = sensor_proxy.get_history(name, days=1, size=24)
    return render_template('sensor.html', sensor = latest, active=['active', '', ''], history=history)

@app.route('/v2/<name>/latest', methods=['GET'])
@login_required
def v2_sensor(name):
    latest = sensor_proxy.get_latest(name)
    return render_template('sensor-latest.html', sensor = latest)


@app.route('/v2/<name>/day', methods=['GET'])
@login_required
def v2_sensor_day(name):
    date = Date.parse(request.args['date']) if 'date' in request.args else Date.today()
    history = sensor_proxy.get_day(name, day=str(date))
    link = '/v2/{}/day?date={}'
    prev_link = link.format(name, str(date.prev))
    next_link = link.format(name, str(date.next))
    nav = Navigation(str(date), prev_link, next_link)
    return render_template('sensor-history.html', name=name, nav=nav, active=['active', '', '', ''], history=history)

@app.route('/v2/<name>/week', methods=['GET'])
@login_required
@http.validate_querystrings(method='GET', parameters=['year', 'week'])
def v2_sensor_week(name):
    current_week = Date.today().week
    year = int(request.args['year']) if 'year' in request.args else current_week.year 
    week_nbr = int(request.args['week']) if 'week' in request.args else  current_week.number
    week = Week(year, week_nbr)

    print(str(week), week.first_day, week.last_day)

    history = sensor_proxy.get_days(name, first=week.first_day, last=week.last_day)
    link = '/v2/{}/week?year={}&week={}'
    prev_link = link.format(name, week.prev.year, week.prev.number)
    next_link = link.format(name, week.next.year, week.next.number)
    nav = Navigation(str(week), prev_link, next_link)
    return render_template('sensor-history.html', name=name, nav=nav, active=['', 'active', '', ''], history=history)

@app.route('/v2/<name>/month', methods=['GET'])
@login_required
def v2_sensor_month(name):
    first = Date.parse(request.args['from']) if 'from' in request.args else Date.today().first_in_month()
    last = Date.parse(request.args['to']) if 'to' in request.args else Date.today().last_in_month()
    history = sensor_proxy.get_days(name, first=first, last=last)
    
    link = '/v2/{}/month?from={}&to={}'
    prev_to = first.prev
    prev_from = prev_to.first_in_month()
    prev_link = link.format(name, prev_from, prev_to)
    next_from = last.next
    next_to = next_from.last_in_month()
    next_link = link.format(name, next_from, next_to)
    nav = Navigation(str(last.datetime.strftime('%B %Y')), prev_link, next_link)
    return render_template('sensor-history.html', name=name, nav=nav, active=['', '', 'active', ''], history=history)


@app.route('/<name>/week', methods=['GET'])
@login_required
def sensor_hours(name):
    latest = sensor_proxy.get_latest(name)
    history = sensor_proxy.get_history(name, days=7, size=48) 
    return render_template('sensor.html', sensor = latest, active=['', 'active', ''], history=history)

@app.route('/<name>/month', methods=['GET'])
@login_required
def sensor_month(name):
    latest = sensor_proxy.get_latest(name)
    history = sensor_proxy.get_history(name, days=30, size=60)
    return render_template('sensor.html', sensor = latest, active=['', '', 'active'], history=history)


@app.route('/solar', methods=['GET'])
@login_required
def solar():
    solar = solar_proxy.get_today()
    solar_history = solar_proxy.get_energy_history(days=7)
    return render_template('solar.html', solar=solar, history=solar_history)

if __name__ == '__main__':
    try:
        logz.init()
        app.run(host='0.0.0.0', port=cfg.web_server.port)
    except Exception:
        logz.exception('Application Exception')
        
