from flask import render_template, jsonify, request, session
from controladores.local import controlador_local as local
from controladores.usuario import controlador_usuario as cuser
from enviar_correos import enviar_mensajecorreo
from hashlib import sha256
import os


def registrar_rutas(app):
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
        
    
    @app.route('/verificar_usuarioDni/<int:id>')
    def verificar_usuarioDni(id):
        try:
            resultado = cuser.verificar_usuarioDni(id)
            
            if resultado:
                datos  = {
                    'id':resultado[0],
                    'nombre': resultado[1],
                    'correo': resultado[2],
                    'telefono': resultado[3],
                }
                return jsonify({'codigo': 1, 'datos': datos})
            else:
                return jsonify({'codigo': 0, 'mensaje': 'No se pudo actualizar el estado del usuario'})
        except Exception as e:
            print(f"Error en verificar_usuarioDni: {e}")
            return jsonify({'codigo': 0, 'mensaje': f'Error al procesar la solicitud: {str(e)}'}), 500
