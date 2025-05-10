import os
from werkzeug.utils import secure_filename
from flask import current_app, flash, redirect, render_template, request, session, url_for
from datetime import datetime
import uuid
from controladores.local import controlador_local
from flask import abort
import re   

# Configuración
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = 'static/assets/img_locales'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generar_nombre_archivo(username, original_filename, file_type):
    """Genera nombres de archivo seguros y organizados"""
    # Sanitizar inputs
    safe_username = secure_filename(username)[:20] or 'usuario'
    safe_name = secure_filename(original_filename.split('.')[0])[:20] or 'imagen'
    
    # Obtener extensión válida
    ext = original_filename.split('.')[-1].lower() if '.' in original_filename else 'jpg'
    ext = ext if ext in ALLOWED_EXTENSIONS else 'jpg'
    
    # Formato: usuario_fechaHora_tipo_nombre.ext
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe_username}_{timestamp}_{file_type}_{safe_name}.{ext}"

def save_uploaded_file(file, subfolder):
    """Guarda archivos con nombres seguros"""
    if file and file.filename and allowed_file(file.filename):
        try:
            username = session.get('username', str(session.get('id', 'default')))
            file_type = subfolder[:-1]  # 'logos' -> 'logo'
            filename = generar_nombre_archivo(username, file.filename, file_type)
            
            upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, subfolder)
            os.makedirs(upload_path, exist_ok=True)
            
            file.save(os.path.join(upload_path, filename))
            return filename
        except Exception as e:
            print(f"Error guardando archivo: {str(e)}")
            return None
    return None

def registrar_rutas(app):
    """Registra todas las rutas relacionadas con locales"""

    @app.route('/pagina_registrar')
    def pagina_registrar():
        id = session.get('id')
        datos = controlador_local.verificarregistrollocal(id)
        return render_template('pages/negocio/negocio/negocio.html', datos=datos)

    @app.route('/registrar_local', methods=['POST'])
    def registrar_local():
        try:
            # Validar archivos
            facebook = request.form.get('facebook', '').strip()
            instagram = request.form.get('instagram', '').strip()

            def format_social_url(input, domain):
                if not input:
                    return None
                
                input = input.replace("@", "")  # Eliminamos @ si existe
                
                # Si ya es una URL válida, la dejamos igual
                if input.startswith(('http://', 'https://')):
                    return input if domain in input else None
                
                # Si es un nombre de usuario, creamos la URL completa
                return f'https://{domain}.com/{input.split("/")[-1]}'

            # Aplicamos el formato
            facebook = format_social_url(facebook, 'facebook')
            instagram = format_social_url(instagram, 'instagram')

            if 'logo' not in request.files or 'banner' not in request.files:
                flash('Debes subir ambas imágenes', 'danger')
                return redirect(url_for('pagina_registrar'))

            logo_file = request.files['logo']
            banner_file = request.files['banner']
            
            # Guardar archivos
            logo_filename = save_uploaded_file(logo_file, 'logos')
            banner_filename = save_uploaded_file(banner_file, 'banners')
            
            if not logo_filename or not banner_filename:
                flash('Formato de imagen no válido (solo: png, jpg, jpeg, gif, webp)', 'danger')
                return redirect(url_for('pagina_registrar'))

            # Preparar datos
            data = {
                'nombre': request.form['nombre'],
                'direccion': request.form['direccion'],
                'tel': request.form['tel'],
                'correo': request.form['correo'],
                'facebook': facebook,
                'instagram': instagram,
                'idUsuario': session.get('id'),
                'logo': logo_filename,
                'banner': banner_filename
            }
            
            # Registrar en DB
            local_id = controlador_local.registrar_local(data)

            if local_id: 
                flash('Local registrado exitosamente!', 'success')
                return redirect(url_for('listar_locales'))
            else:
                flash('Error al guardar en la base de datos', 'danger')
                return redirect(url_for('pagina_registrar'))

        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'danger')
            return redirect(url_for('pagina_registrar'))

    @app.route('/locales')
    def listar_locales():
        id_usuario = session.get('id')
        if not id_usuario:
            flash('Debes iniciar sesión', 'danger')
            return redirect(url_for('login'))
            
        local = controlador_local.verificarregistrollocal(id_usuario)
        
        if local:
            return render_template('pages/negocio/negocio/listar_locales.html', local=local)
        else:
            flash('No tienes locales registrados', 'info')
            return redirect(url_for('pagina_registrar'))