from conexion import obtener_conexion

def consultar_cancha(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """
            select c.descripcion, c.precio, c.puntuacion, c.estado, fo.nombre, fo.foto 
            from CANCHA c 
            inner join FOTO fo on c.idCancha = fo.idCancha
            where c.idCancha = %s
            """
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                cancha = {
                    "descripcion": result[0],
                    "precio": result[1],
                    "puntuacion": result[2],
                    "estado": result[3],
                    "nombre_foto": result[4],
                    "foto": result[5]
                }
                return cancha
            else:
                return None
    finally:
        conexion.close()
        
def consultar_cancha_x_persona(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """
            SELECT * FROM CANCHA ca
            INNER JOIN `LOCAL` lo ON ca.idLocal = lo.idLocal
            WHERE lo.idUsuario = %s
            """
            cursor.execute(query, (id,))
            result = cursor.fetchall()
            canchas = []
            for row in result:
                cancha = {
                    "idCancha": row[0],
                    "descripcion": row[1],
                    "precio": row[2],
                    "puntuacion": row[3],
                    "estado": row[4],
                    "idLocal": row[5],
                    "nombre_foto": row[6],
                    "foto": row[7]
                }
                canchas.append(cancha)
            return canchas
    finally:
        conexion.close()