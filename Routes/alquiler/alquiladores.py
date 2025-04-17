from flask import render_template, request, redirect, url_for, flash
from controladores.tipo_usuario.controlador_tipo_usuario import (
    crear_tipo_usuario,
    obtener_todos_los_tipos_usuarios,
    obtener_tipo_usuario_por_id,
    actualizar_tipo_usuario,
    eliminar_tipo_usuario
)

def registrar_rutas(app):    
    @app.route("/gestionar_tipo_usuario_vendedor", methods=["GET"])
    def gestionar_tipo_usuario_vendedor():
        tipos_usuario = obtener_todos_los_tipos_usuarios() 
        return render_template("tipo_usuario/gestionar_tipo_usuario_vendedor.html", tipos_usuario=tipos_usuario)

    @app.route("/actualizar_tipo_usuario_vendedor/<int:idTipoUsuario>", methods=["GET", "POST"])
    def actualizar_tipo_usuario_vendedor(idTipoUsuario):
        tipo_usuario = obtener_tipo_usuario_por_id(idTipoUsuario)
        
        if tipo_usuario["idTipoUsuario"] != 2:
            flash("No tienes permiso para actualizar este tipo de usuario.")
            return redirect(url_for("gestionar_tipo_usuario_vendedor"))
        
        if request.method == "POST":
            nombre = request.form["nombre"]
            actualizar_tipo_usuario(idTipoUsuario, nombre)
            flash("Tipo de usuario actualizado con éxito.")
            return redirect(url_for("gestionar_tipo_usuario_vendedor"))
        
        return render_template("tipo_usuario/actualizar_tipo_usuario_vendedor.html", tipo_usuario=tipo_usuario)

    @app.route("/eliminar_tipo_usuario_vendedor/<int:idTipoUsuario>", methods=["GET"])
    def eliminar_tipo_usuario_vendedor(idTipoUsuario):
        flash("No tienes permiso para eliminar tipos de usuario.")
        return redirect(url_for("gestionar_tipo_usuario_vendedor"))
