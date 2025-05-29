from flask import redirect, render_template, jsonify, request, session, url_for, current_app
from controladores.canchas import cancha as controlador_cancha_admin
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

def registrar_rutas(app):
    @app.route('/canchass')
    def canchass():
        if session.get('tipo') != "Alquilador":
            return render_template('pages/negocio/canchas/cancha.html')  # Para otros tipos de usuarios

        id_usuario = session.get('id')
        data = controlador_cancha_admin.consultar_cancha_x_persona(id_usuario)
        cantidad_canchas = controlador_cancha_admin.cantidad_canchas(id_usuario)
        tipo_suscripcion = controlador_cancha_admin.tipo_suscripcion(id_usuario)

        print(tipo_suscripcion, cantidad_canchas, data)

        # Deshabilitar canchas si excede el límite
        if (tipo_suscripcion == 'Gratuita' and cantidad_canchas >= 2) or \
        (tipo_suscripcion == 'Paga' and cantidad_canchas >= 4):
            controlador_cancha_admin.desabilitar_canchas(id_usuario)

        # Determinar si se debe activar bloqueo de nuevas canchas
        bloqueo = False
        if (tipo_suscripcion == 'Gratuita' and cantidad_canchas == 1) or \
        (tipo_suscripcion == 'Paga' and cantidad_canchas == 3):
            bloqueo = True

        return render_template('pages/negocio/canchas/cancha.html', data=data, bloqueo=bloqueo, tipo_suscripcion=tipo_suscripcion)



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
        precio_mañana      = request.form['precio_cancha_mañana']
        precio_tarde       = request.form['precio_cancha_tarde']
        precio_noche       = request.form['precio_cancha_noche']
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
            descripcion, precio_mañana, precio_tarde, precio_noche, puntuacion, id_local, id_deporte
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
        return render_template('pages/negocio/canchas/modificar_cancha.html', datos=datos, canchas=canchas, fotos=fotos, id_cancha=id_cancha)

    @app.route('/agregar_horario_cancha/<id>')
    def agregar_horario_cancha(id):
        datos = controlador_cancha_admin.consultar_cancha(id)
        return render_template('pages/negocio/canchas/agregar_horario_cancha.html', id=id, datos=datos)


    @app.route('/moficar_cancha/<int:id>', methods=['POST'])
    def moficar_cancha(id):
    # 1) Recuperar datos del formulario
        descripcion = request.form['descripcion_cancha']
        id_deporte = request.form['tipo_cancha']
        precio_mañana = request.form['precio_cancha_mañana']
        precio_tarde = request.form['precio_cancha_tarde']
        precio_noche = request.form['precio_cancha_noche']
        puntuacion = 0.01
        archivos = request.files.getlist('fotos_nuevas')  # Asegúrate de que este nombre coincida con el de tu formulario

        # 2) Modificar la cancha
        controlador_cancha_admin.modificar_cancha(
            id,
            descripcion,
            precio_mañana,
            precio_tarde,
            precio_noche,
            puntuacion,
            id_deporte
        )

        # 3) Subir nuevas fotos (si hay)
        if archivos:
            for file in archivos:
                if file and file.filename:
                    filename = secure_filename(file.filename)  # Asegura un nombre seguro
                    destino = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(destino)  # Guarda la foto en la carpeta de destino

                    # 4) Insertar la foto en la base de datos
                    controlador_cancha_admin.insertar_foto(
                        id,
                        nombre=filename,
                        ruta=filename
                    )

        # 5) Eliminar las fotos actuales solo si hay nuevas fotos
        # if archivos:
        #     controlador_cancha_admin.eliminar_foto(id)

        # 6) Redirigir al listado de canchas
        return redirect(url_for('canchass'))


    @app.route('/pagina_reservasfiltro/<string:fecha>')
    def pagina_reservasfiltro(fecha):
        print(fecha)

        listas_canchas, horario = controlador_cancha_admin.listar_canchas_idalquilador(session.get('id'),fecha)
        lista_horario = []
        hora_imañana = int(str(horario[1]).split(':')[0])
        hora_fmañana = int(str(horario[2]).split(':')[0])
        hora_itarde = int(str(horario[3]).split(':')[0])
        hora_ftarde = int(str(horario[4]).split(':')[0])
        hora_inoche = int(str(horario[5]).split(':')[0])
        hora_fnoche = int(str(horario[6]).split(':')[0])
        for hrm in range(hora_imañana, hora_fmañana):
            lista_horario.append({
                'hora_inicio': str(hrm)+':00',
                'hora_fin': str(hrm+1)+':00',
                'estado': 'I'
            })
        for hrt in range(hora_itarde, hora_ftarde):
            lista_horario.append({
                'hora_inicio': str(hrt)+':00',
                'hora_fin': str(hrt+1)+':00',
                'estado': 'I'
            })
        for hrn in range(hora_inoche, hora_fnoche):
            lista_horario.append({
                'hora_inicio': str(hrn)+':00',
                'hora_fin': str(hrn+1)+':00',
                'estado': 'I'
            })
        
        
        status = 0
        if listas_canchas:
            status = 1
        return jsonify({
            'status': status,
            'data': listas_canchas,
            'horario': lista_horario
        })
        
    @app.route('/pagina_reservas/')
    def pagina_reservas():
        hoy = datetime.now()
        fechas_listado = list()

        for dia in range(5):
            fechas_listado.append((hoy + timedelta(days=dia)).strftime('%Y-%m-%d'))


        respuesta  = controlador_cancha_admin.listar_canchas_idalquilador(session.get('id'),fechas_listado[0])
        if respuesta:
            listas_canchas = respuesta[0]
            horario = respuesta[1]        
            lista_horario = []
            hora_imañana = int(str(horario[1]).split(':')[0])
            hora_fmañana = int(str(horario[2]).split(':')[0])
            hora_itarde = int(str(horario[3]).split(':')[0])
            hora_ftarde = int(str(horario[4]).split(':')[0])
            hora_inoche = int(str(horario[5]).split(':')[0])
            hora_fnoche = int(str(horario[6]).split(':')[0])
            for hrm in range(hora_imañana, hora_fmañana):
                lista_horario.append({
                    'hora_inicio': str(hrm)+':00',
                    'hora_fin': str(hrm+1)+':00',
                    'estado': 'I'
                })
            for hrt in range(hora_itarde, hora_ftarde):
                lista_horario.append({
                    'hora_inicio': str(hrt)+':00',
                    'hora_fin': str(hrt+1)+':00',
                    'estado': 'I'
                })
            for hrn in range(hora_inoche, hora_fnoche):
                lista_horario.append({
                    'hora_inicio': str(hrn)+':00',
                    'hora_fin': str(hrn+1)+':00',
                    'estado': 'I'
                })
            return render_template('pages/negocio/canchas/lista_cancha.html', listas_canchas = listas_canchas, fechas_listado=fechas_listado,lista_horario=lista_horario)
        else:
            return render_template('pages/negocio/canchas/lista_cancha.html',listas_canchas = {})



    @app.route('/reservar_cancha/<int:id>')
    def reservar_cancha(id):
        hoy = datetime.now()
        dias = [hoy + timedelta(days=i) for i in range(4)]
        fechas_formateadas = [fecha.strftime('%d/%m/%Y') for fecha in dias]
        return render_template('pages/negocio/canchas/reserva_canchas.html', days = fechas_formateadas )
    

    @app.route('/datos_clientejugador/<int:id>')
    def datos_clientejugador(id):
        datos= controlador_cancha_admin.datos_jugadoralquilo(id)
        mensaje = {}
        if datos:
            mensaje['status'] = 1,
            mensaje['valor'] = datos
        else:
            mensaje['status']=0
        return jsonify(mensaje)
    
    @app.route('/alquiler_cancha', methods=['POST'])
    def alquiler_cancha():
        datos = request.get_json()
        respuesta= controlador_cancha_admin.registrar_reserva(datos['fecha'], datos['hora_inicio'], datos['hora_fin'], datos['id_cancha'], datos['id_usuario'])
        mensaje = {}
        if respuesta:
            mensaje['status'] = 1
        else:
            mensaje['status']= 0
        return jsonify(mensaje)
    

    @app.route('/eliminar_reserva/<int:id_reserva>')
    def eliminar_reserva(id_reserva):
        try:
            respuesta = controlador_cancha_admin.eliminar_reserva(id_reserva)
            return jsonify({'status': respuesta})
        except:
            return jsonify({'status': 0})



