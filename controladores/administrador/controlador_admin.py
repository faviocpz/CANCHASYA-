from conexion import obtener_conexion

from conexion import obtener_conexion
from datetime import datetime

def obtener_suscripciones_activas_vencidas():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT
                    SUM(CASE WHEN estado = 'A' AND fecha_fin >= CURDATE() THEN 1 ELSE 0 END) AS suscripciones_activas,
                    SUM(CASE WHEN estado = 'A' AND fecha_fin < CURDATE() THEN 1 ELSE 0 END) AS suscripciones_vencidas
                FROM SUSCRIPCION;
            '''
            cursor.execute(query)
            resultado = cursor.fetchone()
            return {
                'activas': resultado[0] if resultado[0] else 0,
                'vencidas': resultado[1] if resultado[1] else 0
            }
    except Exception as e:
        print(f"Error al obtener suscripciones activas y vencidas: {e}")
        return {'activas': 0, 'vencidas': 0}
    finally:
        conexion.close()

def obtener_ingresos_por_periodo(fecha_inicio, fecha_fin):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT
                    DATE_FORMAT(fecha, '%%Y-%%m') AS mes,
                    SUM(total) AS ingresos_totales
                FROM COMPROBANTE
                WHERE fecha BETWEEN %s AND %s
                GROUP BY mes
                ORDER BY mes;
            '''
            cursor.execute(query, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
            ingresos = [{'mes': row[0], 'total': float(row[1])} for row in resultados]
            return ingresos
    except Exception as e:
        print(f"Error al obtener ingresos por periodo: {e}")
        return []
    finally:
        conexion.close()

def obtener_aliados_activos():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT COUNT(DISTINCT s.idUsuario) AS aliados_activos
                FROM SUSCRIPCION s
                JOIN PLAN p ON s.idPlan = p.idPlan
                WHERE p.tarifa > 0 AND s.estado = 'A' AND s.fecha_fin >= CURDATE();
            '''
            cursor.execute(query)
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error al obtener aliados activos: {e}")
        return 0
    finally:
        conexion.close()

def obtener_historial_pagos(limit=10):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT
                    c.numComprobante,
                    c.fecha,
                    c.subtotal,
                    c.igv,
                    c.total,
                    u.nombre,
                    p.nombre
                FROM COMPROBANTE c
                JOIN SUSCRIPCION s ON c.idSuscripcion = s.idSuscripcion
                JOIN usuario u ON s.idUsuario = u.id
                JOIN PLAN p ON s.idPlan = p.idPlan
                ORDER BY c.fecha DESC
                LIMIT %s;
            '''
            cursor.execute(query, (limit,))
            resultados = cursor.fetchall()
            pagos = []
            for row in resultados:
                pagos.append({
                    'numComprobante': row[0],
                    'fecha': row[1].strftime('%Y-%m-%d'),
                    'subtotal': float(row[2]),
                    'igv': float(row[3]),
                    'total': float(row[4]),
                    'usuario': row[5],
                    'plan': row[6]
                })
            return pagos
    except Exception as e:
        print(f"Error al obtener historial de pagos: {e}")
        return []
    finally:
        conexion.close()

def obtener_suscripciones_por_fecha(fecha_inicio, fecha_fin):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT
                    s.idSuscripcion,
                    s.fecha_ini,
                    s.fecha_fin,
                    s.estado,
                    u.nombre,
                    p.nombre
                FROM SUSCRIPCION s
                JOIN usuario u ON s.idUsuario = u.id
                JOIN PLAN p ON s.idPlan = p.idPlan
                WHERE s.fecha_ini BETWEEN %s AND %s
                ORDER BY s.fecha_ini DESC;
            '''
            cursor.execute(query, (fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
            suscripciones = []
            for row in resultados:
                suscripciones.append({
                    'idSuscripcion': row[0],
                    'fecha_ini': row[1].strftime('%Y-%m-%d'),
                    'fecha_fin': row[2].strftime('%Y-%m-%d'),
                    'estado': row[3],
                    'usuario': row[4],
                    'plan': row[5]
                })
            return suscripciones
    except Exception as e:
        print(f"Error al obtener suscripciones por fecha: {e}")
        return []
    finally:
        conexion.close()

def obtener_proximos_vencimientos(dias=7):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT
                    s.idSuscripcion,
                    s.fecha_fin,
                    u.nombre,
                    p.nombre
                FROM SUSCRIPCION s
                JOIN usuario u ON s.idUsuario = u.id
                JOIN PLAN p ON s.idPlan = p.idPlan
                WHERE s.fecha_fin BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
                AND s.estado = 'A'
                ORDER BY s.fecha_fin ASC;
            '''
            cursor.execute(query, (dias,))
            resultados = cursor.fetchall()
            alertas = []
            for row in resultados:
                alertas.append({
                    'idSuscripcion': row[0],
                    'fecha_fin': row[1].strftime('%Y-%m-%d'),
                    'usuario': row[2],
                    'plan': row[3]
                })
            return alertas
    except Exception as e:
        print(f"Error al obtener próximos vencimientos: {e}")
        return []
    finally:
        conexion.close()


def obtener_suscripciones_activas():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT 
                lo.nombre, lo.tel, lo.correo, 
                su.fecha_ini, su.fecha_fin, 
                con.foto_confirmacion, su.idSuscripcion
                FROM 
                SUSCRIPCION su
                INNER JOIN usuario us ON us.id = su.idUsuario
                INNER JOIN COMPROBANTE con ON con.idSuscripcion = su.idSuscripcion
                INNER JOIN LOCAL lo ON lo.idUsuario = us.id
                WHERE su.estado = 'A' AND su.idPlan = 2;
            '''
            cursor.execute(query)
            resultados = cursor.fetchall()
            suscripciones = []
            for row in resultados:
                suscripciones.append({
                    'nombre': row[0],
                    'telefono': row[1],
                    'correo': row[2],
                    'fecha_inicio': row[3].strftime('%Y-%m-%d'),
                    'fecha_fin': row[4].strftime('%Y-%m-%d'),
                    'foto_confirmacion': row[5],
                    'idSuscripcion': row[6]
                })
            return suscripciones
    except Exception as e:
        print(f"Error al obtener suscripciones activas: {e}")
        return []
    finally:
        conexion.close()
        
def dar_baja_suscripcion(id_suscripcion):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                UPDATE SUSCRIPCION
                SET estado = 'I'
                WHERE idSuscripcion = %s;
            '''
            cursor.execute(query, (id_suscripcion,))
            conexion.commit()
            return True
    except Exception as e:
        print(f"Error al dar de baja la suscripción: {e}")
        return False
    finally:
        conexion.close()