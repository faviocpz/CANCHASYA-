from flask import Flask, render_template, jsonify, request
from controladores.usuario import controlador_usuario as cuser
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/canchas')
def canchas():
    return render_template('pages/canchas.html')

@app.route('/cancha')
def cancha():
    return render_template('pages/cancha.html')

@app.route('/carrito')
def carrito():
    return render_template('pages/carrito.html')

@app.route('/panel')
def panel():
    return render_template('pages/panel.html')

@app.route('/maestra_interna')
def maestra_interna():
    return render_template('base_interna.html')


@app.route('/solicitudes')
def solicitudes():
    return render_template('pages/administrador/solicitudes.html')

@app.route('/registro')
def registro():
    return render_template('pages/registro.html')


@app.route('/registrar_alquilador', methods=['POST'])
def registrar_alquilador():
    try:
        data = {
            'foto': request.files['foto_r'].filename,
            'nombres': request.form['nombres'],
            'dni': request.form['dni'],
            'correo': request.form['correo'],
            'telefono': request.form['telefono']
        }

        respuesta = cuser.crear_usuario(data)
        mensaje = ""
        if(respuesta == 1):
            mensaje = "Se registro correctamente el alquilador"
        elif(respuesta == 2):
            mensaje = "El correo ya existe"
        else:
            return 2
        return jsonify({'codigo': respuesta, 'mensaje': 'Se registro correctamente'})
    except Exception as e:
        return jsonify({'codigo': 0, 'mensaje': f'Error al procesar la solicitud: {str(e)}'}), 500
    

    

if __name__ == '__main__':
    app.run(debug=True)
