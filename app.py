from flask import Flask, render_template
import Routes.local.ruta_presentacion as Rpresentacion
import Routes.seguridad as Rseguridad
import os
import Routes.local.router_local as Rlocal
import Routes.canchas.rutas_canchas as Rcanchas


app = Flask(__name__)
app.secret_key = 'clavesegura'

app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static', 'assets', 'img'
)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('pages/index.html')

Rcanchas.registrar_rutas(app)
Rlocal.registrar_rutas(app)
Rpresentacion.registrar_rutas(app)
Rseguridad.registrar_rutas(app)



if __name__ == '__main__':
    app.run(debug=True)
