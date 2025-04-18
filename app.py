from flask import Flask, render_template, jsonify, request
from controladores.usuario import controlador_usuario as cuser
from hashlib import sha256
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
        dni = request.form['dni']
        correo = request.form['correo']
        codigos = []
        data = {
            'foto': request.files['foto_r'].filename,
            'nombre': request.form['nombres'],
            'dni': dni,
            'correo': correo,
            'telefono': request.form['telefono'],
            'password': sha256(str(request.form['password']).encode('utf-8')).hexdigest()
        }

        respuesta_correo = cuser.verificar_correo(correo)
        respuesta_dni = cuser.verificar_dni(dni)
        
        if (respuesta_correo or respuesta_dni):
            if(respuesta_correo):
                codigos.append('correo')
            elif(respuesta_dni):
                codigos.append('dni')
            codigo = 2
        else:
            cuser.crear_usuario_alquilador(data)
            codigo = 1
        print({'codigo_rpt': codigo, 'rpt_duplicados' : codigos}) 
        return jsonify({'codigo_rpt': codigo, 'rpt_duplicados' : codigos})
    except Exception as e:
        return jsonify({'codigo_rpt': 0, 'mensaje': f'Error al procesar la solicitud: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
