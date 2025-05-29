from conexion import obtener_conexion

def obtener_locales():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """

            SELECT l.idLocal, l.nombre, l.direccion, l.estado, l.banner, COUNT(c.idCancha) AS cantidad,
            GROUP_CONCAT(DISTINCT d.nombre ORDER BY d.nombre SEPARATOR ', ') AS deportes,
            CONCAT(
                'Mañana: ', IFNULL(TIME_FORMAT(h.turno_minicio, '%%H:%%i'), '00:00'), ' - ', IFNULL(TIME_FORMAT(h.turno_mfin, '%%H:%%i'), '00:00'), ' | ',
                'Tarde: ', IFNULL(TIME_FORMAT(h.turno_tinicio, '%%H:%%i'), '00:00'), ' - ', IFNULL(TIME_FORMAT(h.turno_tfin, '%%H:%%i'), '00:00'), ' | ',
                'Noche: ', IFNULL(TIME_FORMAT(h.turno_ninicio, '%%H:%%i'), '00:00'), ' - ', IFNULL(TIME_FORMAT(h.turno_nfin, '%%H:%%i'), '00:00')
            ) AS horario
            FROM LOCAL l LEFT JOIN CANCHA c ON l.idLocal = c.idLocal
                         LEFT JOIN DEPORTE d ON c.idDeporte = d.idDeporte
                         LEFT join HORARIO_ATENCION h on l.idLocal=h.idLocal
            where l.estado = %s
            GROUP BY 
            l.idLocal, l.nombre, l.direccion, l.estado, l.banner, h.turno_minicio, h.turno_mfin, h.turno_tinicio, h.turno_tfin, h.turno_ninicio, h.turno_nfin; 


            """
            cursor.execute(query, ("A",))
            result = cursor.fetchall()
        
        locales = []
        for result in result:
            locales.append({
                    "idLocal": result[0],
                    "nombre": result[1],
                    "direccion": result[2],
                    "estado": result[3],
                    "banner": result[4],
                    "cantidad_cancha":result[5],
                    "Deportes": result[6].split(', ') if result[6] else [],
                    "horario": result[7]
                    
            })
        return locales
    finally:
        conexion.close()

def obtener_deportes():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """

            SELECT d.idDeporte, d.nombre AS deportes FROM DEPORTE d

            """
            cursor.execute(query)
            result = cursor.fetchall()
        
        deportes = []
        for result in result:
            deportes.append({
                    "idDeporte": result[0],
                    "Deportes": result[1] if result[1] else []
                    
            })
        return deportes
    finally:
        conexion.close()

def buscar_locales(nombre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """

            SELECT l.idLocal, l.nombre
            FROM LOCAL l 
            where l.nombre = %s

            """
            cursor.execute(query, (nombre,))
            result = cursor.fetchall()
        
        local = []
        for result in result:
            local.append({
                    "idLocal": result[0],
                    "Nombre": result[1] if result[1] else None
                    
            })
        return local
    finally:
        conexion.close()
