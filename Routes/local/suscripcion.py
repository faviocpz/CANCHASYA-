from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for, current_app
from conexion import obtener_conexion
from controladores.local import controlador_suscripcion
from datetime import datetime, timedelta, time, date
from conexion import obtener_conexion
from werkzeug.utils import secure_filename
import os

def registrar_rutas(app):
    @app.route('/pagos_suscripcion')
    def pagos_suscripcion():
        id_usuario = session.get('id')
        
        suscripcion = controlador_suscripcion.obtener_suscrito(id_usuario)

        id_plan = suscripcion['idPlan'] if suscripcion else None
        fecha_fin = suscripcion['fecha_fin'] if suscripcion else None
        id_suscripcion = suscripcion['idSuscripcion'] if suscripcion else None
        dias_restantes = None

        if fecha_fin:
            # Asegurarse de que ambos sean datetime.datetime
            if isinstance(fecha_fin, datetime):
                fecha_fin_dt = fecha_fin
            elif isinstance(fecha_fin, str):
                fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M:%S")
            elif isinstance(fecha_fin, date):
                fecha_fin_dt = datetime.combine(fecha_fin, time.min)
            else:
                fecha_fin_dt = None

            if fecha_fin_dt:
                dias_restantes = (fecha_fin_dt - datetime.now()).days

        suscripcion_gratuita = (id_plan == 1)
        suscripcion_paga = (id_plan == 2)

        return render_template(
            'pages/negocio/negocio/pagos.html',
            suscripcion_gratuita=suscripcion_gratuita,
            suscripcion_paga=suscripcion_paga,
            dias_restantes=dias_restantes,
            idSuscripcion=id_suscripcion
        )
        
    @app.route('/anular_suscripcion', methods=['POST'])
    def anular_suscripcion():
        data = request.get_json()
        id_suscripcion = data.get('idSuscripcion')
        if not id_suscripcion:
            return jsonify({'error': 'Falta el ID de suscripción'}), 400
        try:
            controlador_suscripcion.anular_suscripcion(id_suscripcion)
            return jsonify({'message': 'Suscripción anulada correctamente.'}), 200
        except Exception as e:
            print(f"[ERROR] Al anular la suscripción: {e}")
            return jsonify({'error': 'Error al anular la suscripción.'}), 500


    @app.route('/ir_a_registrar_suscripcion_gratuita')
    def ir_a_registrar_suscripcion_gratuita():
        return render_template(
            'pages/negocio/negocio/registrar_suscripcion.html',
            id=1,
            fecha_inicio=datetime.now(),
            fecha_fin=datetime.now() + timedelta(days=30)
        )

    @app.route('/ir_a_registrar_suscripcion_paga')
    def ir_a_registrar_suscripcion_paga():
        return render_template(
            'pages/negocio/negocio/registrar_suscripcion.html',
            id=2,
            fecha_inicio=datetime.now(),
            fecha_fin=datetime.now() + timedelta(days=30)
        )
        
    
    
    @app.route('/insertar_suscripcion_gratuita', methods=['POST'])
    def insertar_suscripcion_gratuita():
        data = {
            'idUsuario': session.get('id'),
            'idPlan': 1,
            'fecha_inicio': datetime.now(),
            'fecha_fin': datetime.now() + timedelta(days=30)
        }
        resultado = controlador_suscripcion.registrar_suscripcion_primer_paso(data)
        local = controlador_suscripcion.obtener_detalle_local(session.get('id'))
        if resultado:
            flash('Suscripción gratuita insertada correctamente.', 'success')
            return render_template(
                'pages/negocio/negocio/comprobante_pago.html',
                tipo_suscripcion='GRATUITA',
                nombre_local=local['nombre'],
                direccion=local['direccion'],
                telefono=local['tel'],
                correo=local['correo'],
                subtotal=0.00,
                igv=0.00,
                total=0.00,
                fecha_actual=datetime.now().strftime("%d/%m/%Y %H:%M"),
                resultado = resultado
            )
        flash('Error al insertar la suscripción gratuita.', 'danger')
        return redirect(url_for('pagos_suscripcion'))
    
    
    @app.route('/insertar_suscripcion_paga', methods=['POST'])
    def insertar_suscripcion_paga():
        data = {
            'idUsuario': session.get('id'),
            'idPlan': 2,
            'fecha_inicio': datetime.now(),
            'fecha_fin': datetime.now() + timedelta(days=30)
        }
        resultado = controlador_suscripcion.registrar_suscripcion_primer_paso(data)
        local = controlador_suscripcion.obtener_detalle_local(session.get('id'))
        if resultado:
            flash('Suscripción paga insertada correctamente.', 'success')
            return render_template(
                'pages/negocio/negocio/comprobante_pago.html',
                tipo_suscripcion='PAGA',
                nombre_local=local['nombre'],
                direccion=local['direccion'],
                telefono=local['tel'],
                correo=local['correo'],
                subtotal=20.00,
                igv=3.60,
                total=23.60,
                fecha_actual=datetime.now().strftime("%d/%m/%Y %H:%M"),
                resultado = resultado
            )
        flash('Error al insertar la suscripción gratuita.', 'danger')
        return redirect(url_for('pagos_suscripcion'))


    
    @app.route('/insertar_comprobante_pago', methods=['POST'])
    def insertar_comprobante_pago():
        try:
            # Obtener datos del formulario
            igv = float(request.form['igv'])
            subtotal = float(request.form['subtotal'])
            total = float(request.form['total'])
            id_suscripcion = int(request.form['id_suscripcion'])
            id_usuario = int(request.form['idUsuario'])
            id_forma_pago = 1  # 1 = Yape
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Procesar archivo
            archivo = request.files['comprobante']
            if archivo.filename == '':
                flash("Debes subir un comprobante.", "danger")
                return redirect(request.referrer)

            nombre_seguro = secure_filename(archivo.filename)

            # Crear carpeta si no existe
            carpeta_usuario = os.path.join('static/assets/img/comprobantes', str(id_usuario))
            os.makedirs(carpeta_usuario, exist_ok=True)

            # Guardar el archivo
            ruta_archivo = os.path.join(carpeta_usuario, nombre_seguro)
            archivo.save(ruta_archivo)

            # Ruta relativa a guardar en la base de datos
            ruta_relativa = f'static/assets/img/comprobantes/{id_usuario}/{nombre_seguro}'

            # Guardar en la base de datos
            exito = controlador_suscripcion.insertar_comprobante_paga(
                igv, subtotal, total, fecha, id_suscripcion, ruta_relativa, id_forma_pago
            )

            controlador_suscripcion.confirmar_suscripcion(id_suscripcion)
            if exito:
                flash("Comprobante cargado exitosamente.", "success")
            else:
                flash("Error al guardar el comprobante.", "danger")
            
            return redirect(url_for('pagos_suscripcion'))

        except Exception as e:
            print(f"[ERROR] En ruta insertar_comprobante_pago: {e}")
            flash("Ha ocurrido un error inesperado.", "danger")
            return redirect(request.referrer)

    
    @app.route('/confirmar_suscripcion_gratuita', methods=['POST'])
    def confirmar_suscripcion_gratuita():
        data = request.get_json()

        # Extraer o mapear campos
        id_suscripcion = data.get('idSuscripcion') or data.get('id_suscripcion')
        if not id_suscripcion:
            return jsonify({'error': 'Falta el ID de suscripción'}), 400

        igv = 0.00
        subtotal = 0.00
        total = 0.00
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar suscripción
        controlador_suscripcion.confirmar_suscripcion(
             id_suscripcion
        )

        # Insertar comprobante
        controlador_suscripcion.insertar_comprobante_gratuita(
            igv, subtotal, total, fecha, id_suscripcion
        )

        return jsonify({'message': 'Suscripción gratuita confirmada correctamente.'}), 200

    
    
    
        
        
    

    