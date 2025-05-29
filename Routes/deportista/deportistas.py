from flask import redirect, render_template, jsonify, request, session, url_for, current_app
from controladores.usuario import controlador_usuario  as cusu
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
