from conexion import obtener_conexion

def obtener_locales():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """
            
            select l.idLocal, l.nombre, l.direccion, l.estado, l.banner, count(c.idCancha) as cantidad,
            GROUP_CONCAT(DISTINCT d.nombre ORDER BY d.nombre SEPARATOR ', ') AS deportes
            from LOCAL l left join CANCHA c on l.idLocal = c.idLocal
			             left join DEPORTE d ON c.idDeporte = d.idDeporte
            where l.estado = %s
            GROUP BY 
            l.idLocal, l.nombre, l.direccion, l.estado, l.banner;
            
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
                    "Deportes": result[6].split(', ') if result[6] else []
                    
            })
        return locales
    finally:
        conexion.close()
