from flask import Flask, render_template, jsonify, request, session
from controladores.usuario import controlador_usuario as cuser
from hashlib import sha256
import os
from enviar_correos import enviar_mensajecorreo

app = Flask(__name__)
app.secret_key = 'clavesegura'



@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/logout')
def logout():
    session.clear()
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

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return render_template('pages/login.html')

    correo = session['usuario']
    datos = cuser.obtener_datos_usuario_por_correo(correo)

    if datos:
        return render_template('pages/perfil.html', usuario=datos)
    else:
        return "Usuario no encontrado", 404


@app.route('/maestra_interna')
def maestra_interna():
    return render_template('base_interna.html')

@app.route('/solicitudes')
def solicitudes():
    solicitudes = cuser.retornar_usuario()
    return render_template('pages/administrador/solicitudes.html', solicitudes = solicitudes)

@app.route('/registro')
def registro():
    return render_template('pages/registro.html')


@app.route('/registrar_alquilador', methods=['POST'])
def registrar_alquilador():
    try:
        dni = request.form['dni']
        correo = request.form['correo']
        codigos = []
        foto = request.files['foto_r']
        data = {
            'foto': foto.filename,
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
            id_carpeta = cuser.crear_usuario_alquilador(data)
            carpeta = f"/static/assets/img_usuario/alquilador/{id_carpeta})"
            carpeta = os.path.join(f"static/assets/img_usuario/alquilador/{id_carpeta}")
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
            foto_path = os.path.join(carpeta, 'verificar_img_' + foto.filename)
            foto.save(foto_path)
            codigo = 1
        print({'codigo_rpt': codigo, 'rpt_duplicados' : codigos}) 
        return jsonify({'codigo_rpt': codigo, 'rpt_duplicados' : codigos})
    except Exception as e:
        return jsonify({'codigo_rpt': 0, 'mensaje': f'Error al procesar la solicitud: {str(e)}'}), 500


@app.route('/inicio_sesion', methods=['POST'])
def inicio_sesion():
    correo = request.form['correo']
    password = sha256(str(request.form['password']).encode('utf-8')).hexdigest()
    tipo = request.form.get('tipo')
    id_tipo = 3 if tipo == 'deportista' else 2
    respuesta = cuser.verificar_cuenta(correo,password, id_tipo)
    rpt = {}
    if (respuesta[0] > 0):
        session['usuario'] = correo
        if(tipo == 'deportista'):
            rpt['codigo'] = 1
            rpt['ruta'] = '/'
        elif(tipo == 'aliado'):
            if(respuesta[2] == 1):
                session['tipo'] = "Administrador"
                session['nombre'] = respuesta[3]
                session['token'] = 'x'
            else:
                session['nombre'] = respuesta[3]
                session['vc'] = respuesta[1]
                session['tipo'] = "Alquilador"
                session['token'] = 'x'

            rpt['codigo'] = 1
            rpt['ruta'] = '/maestra_interna'
        else:
            rpt['codigo'] = 0
    else:
        rpt['codigo'] = 0

    return jsonify(rpt)


@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    data = request.get_json()
   
    destinatario = data['email_f']
    asunto = data['asunto_f']
    cuerpo = data['cuerpo_f']

    codigo = enviar_mensajecorreo(destinatario, asunto, cuerpo)

    return jsonify({'codigo': codigo})

@app.route('/cambiar_estado_usuario/<string:estado>/<int:id>')
def cambiar_estado_usuario(estado, id):
    try:
        resultado = cuser.actualizar_estado_verificacion(id, estado)
        if resultado:
            return jsonify({'codigo': 1, 'mensaje': 'Estado del usuario actualizado correctamente'})
        else:
            return jsonify({'codigo': 0, 'mensaje': 'No se pudo actualizar el estado del usuario'})
    except Exception as e:
        return jsonify({'codigo': 0, 'mensaje': f'Error al procesar la solicitud: {str(e)}'}), 500


@app.route('/canchass')
def canchass():
    return render_template('pages/negocio/canchas/cancha.html')

@app.route('/agregar_cancha')
def agregar_cancha():
    return render_template('pages/negocio/canchas/agregar_cancha.html')

@app.route('/negocio')
def negocio():
    return render_template('pages/negocio/negocio.html')

@app.route('/negocio/agregar_negocio')
def agregar_negocio():
    return render_template('pages/negocio/agregar_negocio.html')



if __name__ == '__main__':
    app.run(debug=True)
