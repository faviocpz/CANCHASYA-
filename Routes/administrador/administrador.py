from flask import render_template, request
from controladores.administrador import controlador_admin as controlador_admin

from flask import jsonify
from datetime import datetime

def registrar_rutas_dashboard(app):

    @app.route('/dashboard_suscripciones')
    def dashboard_suscripciones():
        fecha_inicio = request.args.get('fechaInicio')
        fecha_fin = request.args.get('fechaFin')

        if not fecha_inicio or not fecha_fin:
            fecha_fin = datetime.today().strftime('%Y-%m-%d')
            fecha_inicio = (datetime.today().replace(day=1)).strftime('%Y-%m-%d')

        suscripciones = controlador_admin.obtener_suscripciones_activas_vencidas()
        ingresos = controlador_admin.obtener_ingresos_por_periodo(fecha_inicio, fecha_fin)
        aliados = controlador_admin.obtener_aliados_activos()
        historial = controlador_admin.obtener_historial_pagos(limit=10)
        suscripciones_filtro = controlador_admin.obtener_suscripciones_por_fecha(fecha_inicio, fecha_fin)
        alertas = controlador_admin.obtener_proximos_vencimientos(dias=7)

        return render_template('pages/administrador/dashboard_suscripciones.html',
                               suscripciones=suscripciones,
                               ingresos=ingresos,
                               aliados=aliados,
                               historial=historial,
                               suscripciones_filtro=suscripciones_filtro,
                               alertas=alertas,
                               fecha_inicio=fecha_inicio,
                               fecha_fin=fecha_fin)
        
    @app.route('/registro_pagos')
    def registro_pagos():
        
        return render_template('pages/administrador/registro_pagos.html')
    
    @app.route('/api_obtener_suscripciones', methods=['GET'])
    def obtener_suscripciones():
        nota = controlador_admin.obtener_suscripciones_activas()
        return jsonify({
            'suscripciones': nota
        })
    
    @app.route('/dar_baja_suscripcion', methods=['POST'])
    def dar_baja_suscripcion():
        id_suscripcion = request.form.get('idSuscripcion')
        if not id_suscripcion:
            return jsonify({'error': 'ID de suscripción no proporcionado'}), 400
        
        resultado = controlador_admin.dar_baja_suscripcion(id_suscripcion)
        if resultado:
            return jsonify({'success': 'Suscripción dada de baja correctamente'})
        else:
            return jsonify({'error': 'Error al dar de baja la suscripción'}), 500
        
        