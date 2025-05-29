from flask import Flask, render_template
import Routes.local.ruta_presentacion as Rpresentacion
import Routes.seguridad as Rseguridad
import os
from flask import session, redirect, url_for
import Routes.local.router_local as Rlocal
import Routes.canchas.rutas_canchas as Rcanchas
import Routes.deportista.deportistas as Rdeportista
import Routes.administrador.administrador as Rdashboard

import Routes.local.suscripcion as Rsuscripcion
from geopy.geocoders import Nominatim

from geopy.geocoders import Nominatim

def geocode_address(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None




app = Flask(__name__)
app.secret_key = 'clavesegura'

app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static', 'assets', 'img'
)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    direccion = "Los Amautas 235 - Chiclayo"
    coords = geocode_address(direccion)
    print(coords)
    return render_template('pages/index.html')


def error_2013(e):
    return render_template('pages/error/error_500.html')


@app.errorhandler(404)
def error_404(e):
    return render_template('pages/error/error_400.html')

@app.route('/dashboard_ventas')
def dashboard_ventas():
    return render_template('pages/negocio/negocio/dashboard_ventas.html')



Rcanchas.registrar_rutas(app)
Rlocal.registrar_rutas(app)
Rpresentacion.registrar_rutas(app)
Rseguridad.registrar_rutas(app)
Rdeportista.registrar_rutas(app)
Rdashboard.registrar_rutas_dashboard(app)
Rsuscripcion.registrar_rutas(app)

if __name__ == '__main__':
    app.run(debug=True)
