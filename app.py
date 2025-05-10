from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for, current_app
from conexion import obtener_conexion
from controladores.usuario import controlador_usuario as cuser
from controladores.local import controlador_local
from controladores.locales import controlador_locales as local
from controladores.canchas import cancha as controlador_cancha_admin
from hashlib import sha256
import os
from werkzeug.utils import secure_filename
from enviar_correos import enviar_mensajecorreo
import Routes.local.router_local
from datetime import datetime, timedelta

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
    puntuacion       = 0.01
    # dias_sel    = request.form.getlist('dias[]')      # ['Lunes','Martes',...]
    # hora_inicio = request.form['hora_inicio']         # '08:00'
    # hora_fin    = request.form['hora_fin']            # '12:00'
    archivos    = request.files.getlist('foto_cancha')# lista de FileStorage

    # 2) Convertir lista de días a string
                     # "Lunes,Martes,..."

    # 3) Obtener idLocal asociado al usuario en sesión
    id_usuario = session.get('id')
    id_local   = controlador_cancha_admin.id_local(id_usuario)

    # 4) Insertar la CANCHA y obtener su PK
    id_cancha = controlador_cancha_admin.insertar_cancha(
        descripcion, precio, puntuacion, id_local, id_deporte
    )

    # 5) Insertar UN SOLO registro en HORARIO con todos los días
    # controlador_cancha_admin.insertar_horario(
    #     id_cancha,
    #     dias_str,
    #     hora_inicio,
    #     hora_fin,
    #     estado='A'
    # )

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


@app.route('/ir_a_modificar_cancha/<int:id_cancha>')
def ir_a_modificar_cancha(id_cancha):
    # 1) Consultar la cancha por su id
    datos = controlador_cancha_admin.consultar_cancha(id_cancha)
    fotos = controlador_cancha_admin.consultar_fotos(id_cancha)
    # 2) Consultar los tipos de canchas
    canchas = controlador_cancha_admin.tipo_cancha()

    # 3) Enviar los datos al template
    return render_template('pages/negocio/canchas/modificar_cancha.html', datos=datos, canchas=canchas, fotos=fotos)

@app.route('/agregar_horario_cancha/<id>')
def agregar_horario_cancha(id):
    datos = controlador_cancha_admin.consultar_cancha(id)
    return render_template('pages/negocio/canchas/agregar_horario_cancha.html', id=id, datos=datos)

@app.route('/local/<int:idLocal>')
def obtener_local(idLocal):
    # Llamamos al controlador para obtener los datos del local
    local_info, turnos_info, canchas_info, canchas_fotos, cancha_caracteristicas = controlador_local.obtener_informacion_local(idLocal)

    # Pasamos los datos al template (html)
    return render_template('pages/cancha.html', 
                           local_info=local_info, 
                           turnos_info=turnos_info, 
                           canchas_info=canchas_info, 
                           canchas_fotos=canchas_fotos, 
                           cancha_caracteristicas=cancha_caracteristicas)

@app.route('/obtener_horas_disponibles', methods=['GET'])
def obtener_horas_disponibles():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Obtener la fecha seleccionada desde el frontend
        fecha_str = request.args.get('fecha')  # Formato: 'YYYY-MM-DD'
        id_local = request.args.get('idLocal')
       
        print (f"la fecha es {fecha_str}")
        print (f"id del local es {id_local}")
        print("frwjoifjoi")
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

        # Consultamos los turnos de ese local
        cursor.execute("""
            SELECT ha.turno, ha.h_inicio, ha.h_fin
            FROM HORARIO_ATENCION ha
            WHERE ha.idLocal = %s AND ha.estado = 'A'  # Solo turnos activos
        """, (id_local,))
        turnos_info = cursor.fetchall() 
        
        # Consultar las reservas para ese día
        cursor.execute("""
            SELECT h.h_inicio, h.h_fin
            FROM HORARIO h 
            JOIN RESERVA r ON h.idHorario = r.idHorario
            WHERE r.fecha = %s AND h.idCancha IN (SELECT idCancha FROM CANCHA WHERE idLocal = %s)
        """, (fecha, id_local))
        reservas = cursor.fetchall()

        # Filtrar las horas ocupadas
        horas_ocupadas = set()
        for reserva in reservas:
            horas_ocupadas.add(reserva[0].strftime('%H:%M'))  # Hora de inicio
            horas_ocupadas.add(reserva[1].strftime('%H:%M'))  # Hora de fin

        # Preparar las horas disponibles
        turnos = []
        for turno in turnos_info:
            #print(f"Tipo de turno[1]: {type(turno[1])}")
            #print(f"Valor de turno[1]: {turno[1]}")
            #print(f"Tipo de turno[2]: {type(turno[2])}")
            #print(f"Valor de turno[2]: {turno[2]}")
            # Convertir el timedelta a formato HH:MM
            inicio_turno = format_timedelta(turno[1])
            fin_turno = format_timedelta(turno[2])
            
            print(f"Valor de turno[2]: {inicio_turno}")
            # Crear una lista con las horas del turno
            turno_horas = [inicio_turno]
            
            hora = datetime.strptime(inicio_turno, '%H:%M')
            
          
            while hora.strftime('%H:%M') != fin_turno:
                turno_horas.append(hora.strftime('%H:%M'))
                # Sumar 30 minutos
                hora += timedelta(minutes=60)
            # Filtrar las horas disponibles (si no están ocupadas)
            turno_horas = [h for h in turno_horas if h not in horas_ocupadas]

            # Crear el objeto turno
            turno_data = {
                'nombre': turno[0],
                'inicio': format_timedelta(turno[1]),
                'fin': format_timedelta(turno[2]),
                'horas': turno_horas
            }

            turnos.append(turno_data)

        return jsonify({'turnos': turnos})
    
def format_timedelta(td):
    # Obtenemos las horas y minutos desde el timedelta
    total_minutes = int(td.total_seconds() // 60)  # Convertir todo a minutos
    hours = total_minutes // 60  # Dividir para obtener las horas
    minutes = total_minutes % 60  # Obtener los minutos restantes
    
    # Formateamos las horas y minutos en HH:MM
    return f"{hours:02}:{minutes:02}"
    
@app.route('/pagina_reservas/')
def pagina_reservas():
    listas_canchas = controlador_cancha_admin.listar_canchas_idalquilador(session.get('id'))
    print(listas_canchas)
    print(session.get('id'))
    return render_template('pages/negocio/canchas/lista_cancha.html', listas_canchas = listas_canchas)

@app.route('/reservar_cancha/<int:id>')
def reservar_cancha(id):
    hoy = datetime.now()
    dias = [hoy + timedelta(days=i) for i in range(4)]
    fechas_formateadas = [fecha.strftime('%d/%m/%Y') for fecha in dias]
    return render_template('pages/negocio/canchas/reserva_canchas.html', days = fechas_formateadas )



Routes.local.router_local.registrar_rutas(app)


if __name__ == '__main__':
    app.run(debug=True)
