from datetime import datetime, timedelta
from flask import Flask, request, render_template ,redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from pytils import http, log
from pytils.config import cfg
from home_eye.flask_app import FlaskApp
from home_eye.model.user import User
from home_eye.model.solar_proxy import SolarProxy
from home_eye.model.sensor_proxy import SensorProxy
#from home_eye import config

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
        log.init()
        app.run(host='0.0.0.0', port=cfg.web_server.port)
    except Exception:
        log.exception('Application Exception')
        
