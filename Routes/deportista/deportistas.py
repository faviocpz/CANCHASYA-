from flask import redirect, render_template, jsonify, request, session, url_for, current_app, abort
from controladores.usuario import controlador_usuario  as cusu
from controladores.deportista import controlador_deportista  as controlador_deportista

def registrar_rutas(app):
    @app.route('/registrar_deportista', methods = ['POST'])
    def registrar_deportista():
        nombres = request.form['nombres']
        correo = request.form['correo']
        dni = request.form['dni']
        password = request.form['password']
        celular = request.form['celular']
        resultado = cusu.crear_usuario_deportista(nombres, correo, password, celular, dni)
        return jsonify(resultado)

    @app.route('/historial_reservas')
    def historial_reservas():
        # Verificamos que el usuario esté logueado y sea deportista
        print()
        if 'id' not in session or session.get('tipo') != 'Deportista':
            return redirect(url_for('login'))  # O página de error/permiso

        id_usuario = session['id']
        page = request.args.get('page', default=1, type=int)
        per_page = 10

        reservas, total = controlador_deportista.obtener_historial_reservas(id_usuario, page, per_page)
        total_paginas = (total + per_page - 1) // per_page

        return render_template('pages/deportista/historial_reservas.html',
                               reservas=reservas,
                               pagina_actual=page,
                               total_paginas=total_paginas)

    @app.route('/detalle_reserva/<int:id_reserva>')
    def detalle_reserva(id_reserva):
        if 'id' not in session or session.get('tipo') != 'deportista':
            return redirect(url_for('login'))

        id_usuario = session['id']
        reserva = controlador_deportista.obtener_detalle_reserva(id_reserva, id_usuario)
        if not reserva:
            abort(404)

        return render_template('pages/deportista/detalle_reserva.html',
                               reserva=reserva)

