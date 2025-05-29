from flask import render_template, request
from controladores.administrador import controlador_admin as controlador_admin

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
