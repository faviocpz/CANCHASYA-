from conexion import obtener_conexion

def registrar_local(data):
    """Registra un nuevo local en la base de datos."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                INSERT INTO LOCAL (nombre, direccion, tel, correo, facebook, instagram, puntuacion, estado, idUsuario, logo, banner)
                VALUES (%s, %s, %s, %s, %s, %s, NULL, %s, %s, %s, %s)
            '''            
            cursor.execute(query, (
                data['nombre'],
                data['direccion'],
                data['tel'],
                data['correo'],
                data['facebook'],  
                data['instagram'], 
                'A', 
                data['idUsuario'],  
                data['logo'],  
                data['banner'] 
            ))

        conexion.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al registrar el local: {e}")
        return 0  
    finally:
        conexion.close()


def obtener_locales():
    """Obtiene todos los locales registrados en la base de datos."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT idLocal, nombre, direccion, tel, correo, facebook, instagram, puntuacion, estado, idUsuario, logo, banner
                FROM LOCAL
            '''
            cursor.execute(query)
            result = cursor.fetchall()

        # Devolver los locales en formato de lista de diccionarios
        locales = [
            {
                "idLocal": row[0],
                "nombre": row[1],
                "direccion": row[2],
                "tel": row[3],
                "correo": row[4],
                "facebook": row[5],
                "instagram": row[6],
                "puntuacion": float(row[7]),
                "estado": row[8],
                "idUsuario": row[9],
                "logo": row[10],
                "banner": row[11]
            }
            for row in result
        ]
        return locales
    except Exception as e:
        print(f"Error al obtener los locales: {e}")
        return []  
    finally:
        conexion.close()

def verificarregistrollocal(id_usuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT idLocal, nombre, direccion, tel, correo, facebook, instagram, puntuacion, estado, idUsuario, logo, banner
                FROM LOCAL WHERE idUsuario = %s
            '''
            cursor.execute(query, (id_usuario,))
            result = cursor.fetchall()
        
            if result:
                columns = [desc[0] for desc in cursor.description] 
                local_dict = dict(zip(columns, result[0]))  
                return local_dict
            else:
                return None  

    except Exception as e:
        print(f"Error al obtener los locales: {e}")
        return None 
    finally:
        conexion.close()


