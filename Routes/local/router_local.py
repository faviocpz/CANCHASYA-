import os
from werkzeug.utils import secure_filename
from flask import current_app, flash, jsonify, redirect, render_template, request, session, url_for, session 
from datetime import datetime
import uuid
from conexion import obtener_conexion
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
        if not id:
            flash('Debes iniciar sesión primero.', 'danger')
            return redirect(url_for('login'))

        datos = controlador_local.verificarregistrollocal(id)
        
        if datos:  
            flash('Ya tienes un local registrado. No puedes registrar otro.', 'info')
            return redirect(url_for('listar_locales'))
                
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
                
                input = input.replace("@", "") 
                                
                if input.startswith(('http://', 'https://')):
                    return input if domain in input else None
                
                
                return f'https://{domain}.com/{input.split("/")[-1]}'
            
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

        
            data = {
                'nombre': request.form['nombre'],
                'direccion': request.form['direccion'],
                'tel': request.form['tel'],
                'correo': request.form['correo'],
                'facebook': facebook,
                'instagram': instagram,
                'idUsuario': session.get('id'),
                'logo': logo_filename,
                'banner': banner_filename,
                'h_minicio': request.form['h_minicio']+ ':00:00',
                'h_mfin': request.form['h_mfin']+ ':00',
                'h_tinicio': request.form['h_tinicio']+ ':00:00',
                'h_tfin': request.form['h_tfin']+ ':00',
                'h_ninicio': request.form['h_ninicio']+ ':00:00',
                'h_nfin': request.form['h_nfin']+ ':00:00',
            }
            
            # Registrar en DB
            local_id = controlador_local.registrar_local(data)

            if local_id==1: 
                flash('Local registrado exitosamente!', 'success')
                session.update({'local': 1})
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
        


    @app.route('/api/local/editar', methods=['POST'])
    def api_local_editar():
        if 'id' not in session:
            return jsonify({'success': False, 'error': 'No autenticado'}), 401

        usuario_id = session['id']
        data = request.get_json()
        campo = data.get('campo')
        valor = data.get('valor', '').strip()

        # Campos permitidos y reglas básicas
        campos_permitidos = {
            'nombre': (3, 100),
            'direccion': (5, 255),
            'tel': (9, 9),
            'correo': (5, 100),
            'facebook': (0, 255),
            'instagram': (0, 255)
        }

        if campo not in campos_permitidos:
            return jsonify({'success': False, 'error': 'Campo no permitido'}), 400

        min_len, max_len = campos_permitidos[campo]
        if not (min_len <= len(valor) <= max_len):
            return jsonify({'success': False, 'error': f'El campo {campo} debe tener entre {min_len} y {max_len} caracteres'}), 400

        
        if campo == 'telefono' and not valor.isdigit():
            return jsonify({'success': False, 'error': 'Teléfono inválido'}), 400

        if campo == 'correo':
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', valor):
                return jsonify({'success': False, 'error': 'Correo inválido'}), 400
        

        exito, error = controlador_local.actualizar_campo_bd(usuario_id, campo, valor)
        if exito:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': error}), 500



    @app.route('/api/local/editar_imagen', methods=['POST'])
    def editar_imagen_local():
        if 'id' not in session:
            return jsonify({'success': False, 'error': 'No autenticado'}), 401

        usuario_id = session['id']
        campo = request.form.get('campo')

        if campo not in ['logo', 'banner']:
            return jsonify({'success': False, 'error': 'Campo inválido'}), 400

        archivo = request.files.get('imagen')
        if not archivo or not allowed_file(archivo.filename):
            return jsonify({'success': False, 'error': 'Archivo inválido'}), 400

        # Elegir subcarpeta correcta
        subcarpeta = 'logos' if campo == 'logo' else 'banners'
        nuevo_nombre = save_uploaded_file(archivo, subcarpeta)

        if not nuevo_nombre:
            return jsonify({'success': False, 'error': 'Error al guardar imagen'}), 500

        exito, error = controlador_local.actualizar_campo_bd(usuario_id, campo, nuevo_nombre)
        if exito:
            return jsonify({'success': True, 'filename': nuevo_nombre})
        else:
            return jsonify({'success': False, 'error': error}), 500




