from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for, current_app
from controladores.usuario import controlador_usuario as cuser
from controladores.local import controlador_local
from controladores.locales import controlador_locales as local
from controladores.canchas import cancha as controlador_cancha_admin
from hashlib import sha256
import os
from werkzeug.utils import secure_filename
from enviar_correos import enviar_mensajecorreo
import Routes.local.router_local
app = Flask(__name__)
app.secret_key = 'clavesegura'

####### CARPERTA PARA GUARDAR IMAGENES #######
app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static', 'assets', 'img'
)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#############################################

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
    locales = local.obtener_locales()
    return render_template('pages/canchas.html', locales=locales)

@app.route('/api_canchas')
def api_canchas():
    locales = local.obtener_locales()
    return jsonify(locales)

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
        foto_renombrada = f"verificar_img_{correo}.png"

        data = {
            'foto': foto_renombrada,
            'nombre': request.form['nombres'],
            'dni': dni,
            'correo': correo,
            'telefono': request.form['telefono'],
            'password': sha256(str(request.form['password']).encode('utf-8')).hexdigest()
        }

        respuesta_correo = cuser.verificar_correo(correo)
        respuesta_dni = cuser.verificar_dni(dni)
        
        if respuesta_correo or respuesta_dni:
            if respuesta_correo:
                codigos.append('correo')
            elif respuesta_dni:
                codigos.append('dni')
            codigo = 2 
        else:
            foto_path = os.path.join("static/assets/img_usuario/alquilador", foto_renombrada)
            foto.save(foto_path)
            
            usuario_id = cuser.crear_usuario_alquilador(data)

            if usuario_id:
                codigo = 1
            else:
                codigo = 0  

        return jsonify({'codigo_rpt': codigo, 'rpt_duplicados': codigos})

    except Exception as e:
        return jsonify({'codigo_rpt': 0, 'mensaje': f'Error al procesar la solicitud: {str(e)}'}), 500

@app.route('/actualizar_foto_verificacion', methods=['POST'])
def actualizar_foto_verificacion():
    try:
        foto = request.files['foto_perfil']
        correo = request.form['correo']

        if not foto:
            return jsonify({'codigo_rpt': 0, 'mensaje': 'No se recibió ninguna foto'}), 400
        
        carpeta = f"static/assets/img_usuario/alquilador/"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        foto_filename = f"verificar_img_{correo}.png"
        foto_path = os.path.join(carpeta, foto_filename)
        foto.save(foto_path)

        data = {
            'foto': foto_filename,
            'correo': correo
        }

        resultado = cuser.actualizar_foto_verificacion(data)

        if resultado:
            return jsonify({'codigo_rpt': 1, 'mensaje': 'Foto actualizada correctamente.'})
        else:
            return jsonify({'codigo_rpt': 0, 'mensaje': 'Hubo un problema al actualizar la foto.'})

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
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
                session['id'] = respuesta[5]
                session['tipo'] = "Administrador"
                session['nombre'] = respuesta[3]
                session['token'] = 'x'
            else:
                session['id'] = respuesta[5]
                session['nombre'] = respuesta[3]
                session['vc'] = respuesta[1]
                session['tipo'] = "Alquilador"
                session['token'] = 'x'

            rpt['codigo'] = 1
            rpt['ruta'] = '/canchass'
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
    data = controlador_cancha_admin.consultar_cancha_x_persona(session.get('id'))
    return render_template('pages/negocio/canchas/cancha.html', data=data)

@app.route('/api/cancha/<int:id_cancha>')
def api_cancha(id_cancha):
    data = controlador_cancha_admin.consultar_detalle_cancha(id_cancha)
    if not data:
        return jsonify({"error": "Cancha no encontrada"}), 404
    return jsonify(data)

@app.route('/agregar_cancha')
def agregar_cancha():
    id_local = controlador_cancha_admin.id_local(session.get('id'))
    canchas = controlador_cancha_admin.tipo_cancha()
    return render_template('pages/negocio/canchas/agregar_cancha.html', canchas=canchas)


@app.route('/insertar_cancha', methods=['POST'])
def insertar_cancha():
    # 1) Recuperar datos del formulario
    descripcion = request.form['descripcion_cancha']
    id_deporte  = request.form['tipo_cancha']
    precio      = request.form['precio_cancha']
    puntuacion       = request.form['puntuacion_cancha']   
    dias_sel    = request.form.getlist('dias[]')      # ['Lunes','Martes',...]
    hora_inicio = request.form['hora_inicio']         # '08:00'
    hora_fin    = request.form['hora_fin']            # '12:00'
    archivos    = request.files.getlist('foto_cancha')# lista de FileStorage

    # 2) Convertir lista de días a string
    dias_str = ','.join(dias_sel)                     # "Lunes,Martes,..."

    # 3) Obtener idLocal asociado al usuario en sesión
    id_usuario = session.get('id')
    id_local   = controlador_cancha_admin.id_local(id_usuario)

    # 4) Insertar la CANCHA y obtener su PK
    id_cancha = controlador_cancha_admin.insertar_cancha(
        descripcion, precio, puntuacion, id_local, id_deporte
    )

    # 5) Insertar UN SOLO registro en HORARIO con todos los días
    controlador_cancha_admin.insertar_horario(
        id_cancha,
        dias_str,
        hora_inicio,
        hora_fin,
        estado='A'
    )

    # 6) Guardar las fotos (hasta 3) en disco y BD
    for file in archivos:
        if file and file.filename:
            filename = secure_filename(file.filename)
            destino  = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(destino)
            controlador_cancha_admin.insertar_foto(
                id_cancha,
                nombre=filename,
                ruta=filename
            )

    # 7) Redirigir al listado de canchas
    return redirect(url_for('canchass'))



@app.route('/agregar_horario_cancha/<id>')
def agregar_horario_cancha(id):
    datos = controlador_cancha_admin.consultar_cancha(id)
    return render_template('pages/negocio/canchas/agregar_horario_cancha.html', id=id, datos=datos)

@app.route('/local/<int:idLocal>')
def obtener_local(idLocal):    
    local_info = controlador_local.obtener_informacion_local(idLocal)
    return render_template('pages/cancha.html', local_info=local_info)


@app.route('/pagina_reservas/')
def pagina_reservas():
    return render_template('pages/negocio/canchas/reserva_cancha.html')


Routes.local.router_local.registrar_rutas(app)


if __name__ == '__main__':
    app.run(debug=True)
