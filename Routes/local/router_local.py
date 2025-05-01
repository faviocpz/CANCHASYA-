from flask import app, flash, redirect, render_template, request, session, url_for
from controladores.local import controlador_local 

def registrar_rutas(app):
    @app.route('/pagina_registrar')
    def pagina_registrar():
        id = session.get('id')
        datos = controlador_local.verificarregistrollocal(id)
        return render_template('pages/negocio/negocio/negocio.html', datos = datos) 


    @app.route('/registrar_local', methods=['POST'])
    def registrar_local():
        try:
            data = {
                'nombre': request.form['nombre'],
                'direccion': request.form['direccion'],
                'tel': request.form['tel'],
                'correo': request.form['correo'],
                'facebook': request.form['facebook'],
                'instagram': request.form['instagram'],
                'idUsuario': session.get('id'),
                'logo': request.files['logo'].filename,
                'banner': request.files['banner'].filename
            }
            
            local_id = controlador_local.registrar_local(data)

            if local_id: 
                flash('Local registrado exitosamente.', 'success')
                return redirect(url_for('listar_locales'))  
            else:
                flash('Hubo un problema al registrar el local.', 'danger')
                return redirect(url_for('pagina_registrar'))

        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
            return redirect(url_for('pagina_registrar'))

    @app.route('/locales', methods=['GET'])
    def listar_locales():
        id_usuario = session.get('id') 
        local = controlador_local.verificarregistrollocal(id_usuario)
        print(f"Local para el usuario {id_usuario}: {local}") 
        if local: 
            return render_template('pages/negocio/negocio/listar_locales.html', local=local)
        else:
            flash('No tienes un local registrado', 'danger')
            return redirect(url_for('pagina_registrar'))
