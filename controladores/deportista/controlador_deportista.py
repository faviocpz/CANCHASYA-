from conexion import obtener_conexion

def obtener_historial_reservas(id_usuario, page=1, per_page=10):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Conteo total de reservas para paginación
            cursor.execute('''
                SELECT COUNT(*) 
                FROM RESERVA 
                WHERE idUsuario = %s
            ''', (id_usuario,))
            total = cursor.fetchone()[0]
            
            # Consulta paginada con datos básicos
            cursor.execute('''
                SELECT
                  r.idReserva,
                  r.fecha,
                  l.nombre AS nombre_local,
                  d.nombre AS deporte,
                  c.preciom AS precio
                FROM RESERVA r
                JOIN CANCHA c ON r.idCancha = c.idCancha
                JOIN LOCAL l ON c.idLocal = l.idLocal
                JOIN DEPORTE d ON c.idDeporte = d.idDeporte
                WHERE r.idUsuario = %s
                ORDER BY r.fecha DESC, r.hora_inicio DESC
                LIMIT %s OFFSET %s;
            ''', (id_usuario, per_page, offset))
            
            reservas = []
            for row in cursor.fetchall():
                reservas.append({
                    'idReserva': row[0],
                    'fecha': row[1].strftime('%Y-%m-%d'),
                    'nombre_local': row[2],
                    'deporte': row[3],
                    'precio': float(row[4])
                })
            return reservas, total
    except Exception as e:
        print(f"Error al obtener historial de reservas: {e}")
        return [], 0
    finally:
        conexion.close()

def obtener_detalle_reserva(id_reserva, id_usuario):
    conexion = obtener_conexion()

    def formato_hora(td):
        if td is None:
            return None
        total_seconds = int(td.total_seconds())
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        segundos = total_seconds % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    try:
        with conexion.cursor() as cursor:
            cursor.execute('''
                SELECT
                  r.idReserva,
                  r.fecha,
                  r.hora_inicio,
                  r.hora_fin,
                  l.nombre AS nombre_local,
                  l.direccion,
                  l.logo,
                  d.nombre AS deporte,
                  c.descripcion AS descripcion_cancha,
                  c.preciom AS precio
                FROM RESERVA r
                JOIN CANCHA c ON r.idCancha = c.idCancha
                JOIN LOCAL l ON c.idLocal = l.idLocal
                JOIN DEPORTE d ON c.idDeporte = d.idDeporte
                WHERE r.idReserva = %s
                  AND r.idUsuario = %s;
            ''', (id_reserva, id_usuario))

            row = cursor.fetchone()
            if row:
                return {
                    'idReserva': row[0],
                    'fecha': row[1].strftime('%Y-%m-%d'),
                    'hora_inicio': formato_hora(row[2]),
                    'hora_fin': formato_hora(row[3]),
                    'nombre_local': row[4],
                    'direccion': row[5],
                    'logo': row[6],
                    'deporte': row[7],
                    'descripcion_cancha': row[8],
                    'precio': float(row[9])
                }
            else:
                return None
    except Exception as e:
        print(f"Error al obtener detalle de reserva: {e}")
        return None
    finally:
        conexion.close()
