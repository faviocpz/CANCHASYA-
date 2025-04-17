from conexion import obtener_conexion

def verificar_tipo_usuario_existe(nombre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT COUNT(*) FROM TIPO_USUARIO WHERE nombre = %s"""
            cursor.execute(query, (nombre,))
            result = cursor.fetchone()
        
        return result[0] > 0
    finally:
        conexion.close()

def crear_tipo_usuario(nombre):
    if verificar_tipo_usuario_existe(nombre):
        print("El tipo de usuario ya existe.")
        return

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """INSERT INTO TIPO_USUARIO (nombre) VALUES (%s)"""
            cursor.execute(query, (nombre,))
        conexion.commit()
        print("Tipo de usuario creado con éxito.")
    finally:
        conexion.close()

def obtener_tipo_usuario_por_id(idTipoUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT idTipoUsuario, nombre FROM TIPO_USUARIO WHERE idTipoUsuario = %s"""
            cursor.execute(query, (idTipoUsuario,))
            result = cursor.fetchone()
        
        if result:
            return {"idTipoUsuario": result[0], "nombre": result[1]}
        else:
            return None
    finally:
        conexion.close()

def obtener_todos_los_tipos_usuarios():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """SELECT idTipoUsuario, nombre FROM TIPO_USUARIO"""
            cursor.execute(query)
            result = cursor.fetchall()
        
        tipos_usuario = []
        for row in result:
            tipos_usuario.append({"idTipoUsuario": row[0], "nombre": row[1]})
        
        return tipos_usuario
    finally:
        conexion.close()

def actualizar_tipo_usuario(idTipoUsuario, nombre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """UPDATE TIPO_USUARIO SET nombre = %s WHERE idTipoUsuario = %s"""
            cursor.execute(query, (nombre, idTipoUsuario))
        conexion.commit()
        print("Tipo de usuario actualizado con éxito.")
    finally:
        conexion.close()

def eliminar_tipo_usuario(idTipoUsuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """DELETE FROM TIPO_USUARIO WHERE idTipoUsuario = %s"""
            cursor.execute(query, (idTipoUsuario,))
        conexion.commit()
        print("Tipo de usuario eliminado con éxito.")
    finally:
        conexion.close()
