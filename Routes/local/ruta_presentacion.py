from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for, current_app
from conexion import obtener_conexion
from controladores.local import controlador_local
from datetime import datetime, timedelta
from conexion import obtener_conexion

def registrar_rutas(app):
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
            id_cancha = request.args.get('idCancha')
        
            print (f"la fecha es {fecha_str}")
            print (f"id del local es {id_local}")
            print (f"id de la cancha es {id_cancha}")
            print("frwjoifjoi")
            # Convertir la fecha a un objeto datetime
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

            # Consultamos los turnos de ese local
            cursor.execute("""
                SELECT turno_minicio, turno_mfin, turno_tinicio, turno_tfin, turno_ninicio, turno_nfin
                FROM HORARIO_ATENCION
                WHERE idLocal = %s
            """, (id_local,))
            turnos_brutos = cursor.fetchone()

            turnos_info = [
                ('Mañana', turnos_brutos[0], turnos_brutos[1]),
                ('Tarde', turnos_brutos[2], turnos_brutos[3]),
                ('Noche', turnos_brutos[4], turnos_brutos[5]),
            ]

            
            # Consultar las reservas para ese día
            cursor.execute("""
                SELECT r.hora_inicio, r.hora_fin
                FROM RESERVA r 
                WHERE r.fecha = %s AND r.idCancha = %s
            """, (fecha, id_cancha))
            reservas = cursor.fetchall()

            # Filtrar las horas ocupadas
            horas_ocupadas = set()
            for reserva in reservas:
                horas_ocupadas.add(format_timedelta(reserva[0]))  # Hora de inicio
                horas_ocupadas.add(format_timedelta(reserva[1]))  # Hora de fin

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
                turno_horas = []
                
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
    @app.route('/registrar_puntuacion', methods=['POST'])
    def registrar_puntuacion():
        id_cancha = request.form.get('idCancha')  # Ahora capturamos el idCancha del formulario
        puntuacion = request.form.get('puntuacion')  # Puntuación seleccionada
        idLocal = request.form.get('idLocal')  
        # Lógica para almacenar la puntuación en la base de datos
        if id_cancha and puntuacion:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO PUNTUACION_CANCHA (idCancha, puntaje)
                VALUES (%s, %s)
            """, (id_cancha, puntuacion))
            conexion.commit()
            cursor.close()
            conexion.close()

            # Si todo está bien, enviar una respuesta de éxito
            #return jsonify({'success': True})
            return redirect(url_for('obtener_local', idLocal=idLocal))

        return jsonify({'success': False, 'message': 'Puntuación inválida.'})
def format_timedelta(td):
    # Obtenemos las horas y minutos desde el timedelta
    total_minutes = int(td.total_seconds() // 60)  # Convertir todo a minutos
    hours = total_minutes // 60  # Dividir para obtener las horas
    minutes = total_minutes % 60  # Obtener los minutos restantes
    
    # Formateamos las horas y minutos en HH:MM
    return f"{hours:02}:{minutes:02}"    
