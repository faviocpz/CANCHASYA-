from conexion import obtener_conexion
import random
from hashlib import sha256


def verificar_cuenta(correo, contraseña, tipo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            if tipo == 2:
                query = ''' 
                            select count(*), us.verificacion_cuenta, us.idTipoUsuario, us.nombre, us.token, us.id, us.telefono  AS telefono
                            from usuario as us where us.correo = %s
                            and contraseña = %s
                            and (idTipoUsuario = 1 or idTipoUsuario = 2) and estado_cuenta = 1;
                        '''
            else:
                query = ''' 
                            select count(*), us.verificacion_cuenta, us.idTipoUsuario, us.nombre, us.token, us.id, us.telefono  AS telefono
                            from usuario as us where us.correo = %s
                            and contraseña = %s
                            and idTipoUsuario = 3 and estado_cuenta = 1;
                        '''
            cursor.execute(query, (correo, contraseña))
            result = cursor.fetchone()
            if result and result[0] > 0:
                session['telefono'] = result[6]
        return result if result[0] > 0 else [0]
    finally:
        conexion.close()


def actualizar_estado_verificacion(id_usuario, nuevo_estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''UPDATE usuario 
                       SET verificacion_cuenta = %s 
                       WHERE id = %s'''
            cursor.execute(query, (nuevo_estado, id_usuario))
        conexion.commit()
        return 1
    except Exception as e:
        print("Error al actualizar verificación:", e)
        return 0
    finally:
        conexion.close()



def verificar_dni(dni):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = ''' 
                        select count(*) from usuario as us where us.dni = %s 
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
                        select count(*) from usuario as us where us.correo = %s 
                        '''
            cursor.execute(query, (correo,))
            result = cursor.fetchone()
        return result[0] > 0
    finally:
        conexion.close()

def creador_token():
    numero = str(random.randint(1,1024))
    token = sha256(numero.encode('utf-8')).hexdigest()
    return token

def crear_usuario_alquilador(data):
    conexion = obtener_conexion()
    try:
        print("entro")
        with conexion.cursor() as cursor:
            query = '''INSERT INTO usuario (nombre, dni, correo, telefono, foto_verificacion, contraseña, token, estado_cuenta, verificacion_cuenta, idTipoUsuario)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(query, (data['nombre'], data['dni'], data['correo'], data['telefono'],
                                   data['foto'], data['password'], creador_token(), True, 'E', 2))
        
        conexion.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e)  # Mostrar error real
        return 0
    finally:
        conexion.close()

def retornar_usuario():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''  
                    select * from usuario where idTipoUsuario = 2 and verificacion_cuenta = 'E' 
                        '''
            cursor.execute(query, ())
        return cursor.fetchall()
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

def obtener_datos_usuario_por_correo(correo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """
                SELECT nombre, dni, correo, telefono, verificacion_cuenta, idTipoUsuario
                FROM usuario
                WHERE correo = %s
            """
            cursor.execute(query, (correo,))
            resultado = cursor.fetchone()

        if resultado:
            return {
                'nombre': resultado[0],
                'dni': resultado[1],
                'correo': resultado[2],
                'telefono': resultado[3],
                'verificacion_cuenta': resultado[4],
                'idTipoUsuario': resultado[5]
            }
        else:
            return None
    finally:
        conexion.close()

def actualizar_foto_verificacion(data):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                UPDATE usuario
                SET foto_verificacion = %s,
                    verificacion_cuenta = 'E'
                WHERE correo = %s
            '''
            cursor.execute(query, (data['foto'], data['correo']))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al actualizar la foto de verificación:", e)
        return False
    finally:
        conexion.close()







