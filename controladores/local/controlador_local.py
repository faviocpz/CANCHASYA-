from conexion import obtener_conexion
from flask import session
from datetime import datetime
def registrar_local(data):    
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
                data['facebook'] if data['facebook'] else None, 
                data['instagram'] if data['instagram'] else None, 
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

def obtener_informacion_local(id_local):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Consulta de la información del local y las canchas asociadas
    cursor.execute("""
        SELECT l.nombre, l.direccion, l. correo, l.tel, l.facebook, l.instagram, l.banner, l.tel
        FROM LOCAL l 
        WHERE l.idLocal = %s
    """, (id_local,))
    local_info = cursor.fetchall()
     # Consulta para obtener los turnos activos
    cursor.execute("""
        SELECT ha.turno, ha.h_inicio, ha.h_fin
        FROM HORARIO_ATENCION ha
        WHERE ha.idLocal = %s AND ha.estado = 'A'  # Solo turnos activos
    """, (id_local,))
    turnos_info = cursor.fetchall()  # Obtener todos los turnos activos
    # Formateamos las horas eliminando los segundos
    for i, turno in enumerate(turnos_info):
        # Convertimos la tupla a una lista para poder modificar los valores
        turno = list(turno)
        
        # Convertimos los tiempos de 'h_inicio' y 'h_fin' a 'HH:MM'
        turno[1] = turno[1].strftime('%H:%M') if isinstance(turno[1], datetime) else turno[1]  # Se toma solo HH:MM
        turno[2] = turno[2].strftime('%H:%M') if isinstance(turno[2], datetime) else turno[2]  # Se toma solo HH:MM

        # Asignamos el nombre del turno (si quieres truncar el nombre)
        turno[0] = turno[0]
        print(turno)

    # Consulta para obtener las canchas del local
    cursor.execute("""
        SELECT c.idCancha, c.descripcion, c.puntuacion, c.precio
        FROM CANCHA c
        WHERE c.idLocal = %s
    """, (id_local,))
    canchas_info = cursor.fetchall()
    # Consulta para obtener las fotos de cada cancha
    cursor.execute("""
        SELECT f.idCancha, f.foto
    FROM FOTO f
    WHERE f.idCancha IN (SELECT c.idCancha FROM CANCHA c WHERE c.idLocal = %s)
    """, (id_local,))
    fotos_info = cursor.fetchall()
    # Organizar las fotos por cancha
    canchas_fotos = {}
    for foto in fotos_info:
        id_cancha = foto[0]
        if id_cancha not in canchas_fotos:
            canchas_fotos[id_cancha] = []
        canchas_fotos[id_cancha].append(foto[1])  # Añadir el nombre de la foto
    # Consulta para obtener las características de la cancha
   # Inicializa un diccionario para almacenar las características por cancha
    # En la función obtener_informacion_local
    cancha_caracteristicas = {}

    for cancha in canchas_info:
        id_cancha = cancha[0]  # Toma el id de la cancha
        print(f"ID de la cancha: {id_cancha}") 
        cursor.execute("""
            SELECT ca.nombre
            FROM CANCHA_CARACTERISTICA cc
            JOIN CARACTERISTICA ca ON cc.idCaracteristica = ca.idCaracteristica
            WHERE cc.idCancha = %s
        """, (id_cancha,))

        # Obtén las características de esa cancha
        características = cursor.fetchall()

        # Guarda las características de la cancha
        cancha_caracteristicas[id_cancha] = [caracteristica[0] for caracteristica in características]
    
    telefono = session.get('telefono')
    if telefono:
        # úsalo como necesites
        print (f"El teléfono del usuario es {telefono}")
    else:
        print ("No hay usuario logueado.")
    cursor.close()
    conexion.close()

    return local_info, turnos_info, canchas_info, canchas_fotos, cancha_caracteristicas

    cursor.close()
    conexion.close()

    return local_info
