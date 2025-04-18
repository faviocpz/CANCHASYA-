from conexion import obtener_conexion

def verificar_dni(dni):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = ''' 
                        select id from usuario as us where us.dni = %s 
                        '''
            cursor.execute(query, (dni,))
            result = cursor.fetchone()
        return result[0] > 0
    finally:
        conexion.close()

def verificar_correo(correo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = ''' 
                        select id from usuario as us where us.correo = %s 
                        '''
            cursor.execute(query, (correo,))
            result = cursor.fetchone()
        return result[0] > 0
    finally:
        conexion.close()

def crear_usuario_alquilador(data):
    existe_usuario = verificar_dni(data['dni'])
    existe_correo = verificar_correo(data['correo'])
    conexion = obtener_conexion()
    
    existe = list()
    if(existe_correo or existe_usuario):
        if (existe_usuario):
            existe.append(2)
        if(existe_correo):
            existe.append(3)
        return existe
    try:
        with conexion.cursor() as cursor:
            query = ''''INSERT INTO usuario (nombre, dni, correo, telefono, foto_verificacion, contraseña, token, estado_cuenta, verificacion_cuenta)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(query, ())
        conexion.commit()
        return 1
    except:
        return 3
    finally:
        conexion.close()

def obtener_usuario_por_id(idUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT idUsuario, username, estado, idTipoUsuario 
                       FROM USUARIO WHERE idUsuario = %s"""
            cursor.execute(query, (idUsuario,))
            result = cursor.fetchone()
        
        if result:
            return {"idUsuario": result[0], "username": result[1], "estado": result[2], "idTipoUsuario": result[3]}
        else:
            return None
    finally:
        conexion.close()        

def obtener_todos_los_usuarios():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT idUsuario, username, estado, idTipoUsuario 
                       FROM USUARIO"""
            cursor.execute(query)
            result = cursor.fetchall()
        
        usuarios = []
        for row in result:
            usuarios.append({"idUsuario": row[0], "username": row[1], "estado": row[2], "idTipoUsuario": row[3]})
        
        return usuarios
    finally:
        conexion.close()

def actualizar_usuario(idUsuario, username, contraseña, estado, idTipoUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """UPDATE USUARIO 
                       SET username = %s, contraseña = %s, estado = %s, idTipoUsuario = %s
                       WHERE idUsuario = %s"""
            cursor.execute(query, (username, contraseña, estado, idTipoUsuario, idUsuario))
        conexion.commit()
    finally:
        conexion.close()

def eliminar_usuario(idUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """DELETE FROM USUARIO WHERE idUsuario = %s"""
            cursor.execute(query, (idUsuario,))
        conexion.commit()
    finally:
        conexion.close()

def autenticar_usuario(username, contraseña):
    
    if not verificar_usuario_existe(username):
        print("El usuario no existe.")
        return None

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT idUsuario FROM USUARIO WHERE username = %s AND contraseña = %s"""
            cursor.execute(query, (username, contraseña))
            result = cursor.fetchone()
        
        if result:
            return result[0]  
        else:
            print("Contraseña incorrecta.")
            return None
    finally:
        conexion.close()

def cambiar_contraseña(idUsuario, nueva_contraseña):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """UPDATE USUARIO SET contraseña = %s WHERE idUsuario = %s"""
            cursor.execute(query, (nueva_contraseña, idUsuario))
        conexion.commit()
    finally:
        conexion.close()

def habilitar_usuario(idUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """UPDATE USUARIO SET estado = 'A' WHERE idUsuario = %s"""
            cursor.execute(query, (idUsuario,))
        conexion.commit()
    finally:
        conexion.close()

def deshabilitar_usuario(idUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """UPDATE USUARIO SET estado = 'I' WHERE idUsuario = %s"""
            cursor.execute(query, (idUsuario,))
        conexion.commit()
    finally:
        conexion.close()

def obtener_tipo_usuario(idUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT idTipoUsuario FROM USUARIO WHERE idUsuario = %s"""
            cursor.execute(query, (idUsuario,))
            result = cursor.fetchone()
        
        if result:
            return result[0]  
        else:
            return None
    finally:
        conexion.close()

def cambiar_tipo_usuario(idUsuario, nuevo_idTipoUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """UPDATE USUARIO SET idTipoUsuario = %s WHERE idUsuario = %s"""
            cursor.execute(query, (nuevo_idTipoUsuario, idUsuario))
        conexion.commit()
    finally:
        conexion.close()

def verificar_usuario_existe(username):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT COUNT(*) FROM USUARIO WHERE username = %s"""
            cursor.execute(query, (username,))
            result = cursor.fetchone()
         
        return result[0] > 0
    finally:
        conexion.close()














