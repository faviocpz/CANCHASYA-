from datetime import datetime

from flask import current_app, session
from Routes.local.router_local import save_uploaded_file
from conexion import obtener_conexion
from flask import session
from datetime import datetime
from werkzeug.utils import secure_filename
import os



def obtener_suscripcion():
    """Obtiene todos los locales registrados en la base de datos."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT idPlan, nombre, tarifa, descripcion FROM PLAN;
            '''
            cursor.execute(query)
            result = cursor.fetchall()

        # Devolver los locales en formato de lista de diccionarios
        locales = [
            {
                "idPlan": row[0],
                "nombre": row[1],
                "tarifa": row[2],
                "descripcion": row[3]                
            }
            for row in result
        ]
        return locales
    except Exception as e:
        print(f"Error al obtener las suscripciones : {e}")
        return []  
    finally:
        conexion.close()
        
        
import traceback

def registrar_suscripcion_primer_paso(data):
    conexion = None
    try:
        print("[INFO] Intentando conectar a la base de datos...")
        conexion = obtener_conexion()
        print("[INFO] Conexión establecida.")

        with conexion.cursor() as cursor:
            query = '''
                INSERT INTO SUSCRIPCION (idUsuario, idPlan, fecha_ini, fecha_fin, estado)
                VALUES (%s, %s, %s, %s, %s)
            '''
            valores = (
                data.get('idUsuario'),
                data.get('idPlan'),
                data.get('fecha_inicio'),
                data.get('fecha_fin'),
                'I'  # Estado activo
            )
            print(f"[DEBUG] Query a ejecutar:\n{query}")
            print(f"[DEBUG] Valores a insertar: {valores}")

            cursor.execute(query, valores)
            ultimo_id = cursor.lastrowid
            conexion.commit()
            print("[INFO] Suscripción registrada correctamente.")
            return ultimo_id

    except Exception as e:
        if conexion:
            conexion.rollback()
        print("[ERROR] No se pudo registrar la suscripción.")
        print(f"[ERROR] Exception: {e}")
        print(traceback.format_exc())
        return 0

    finally:
        if conexion:
            conexion.close()
            print("[INFO] Conexión cerrada.")




def obtener_suscrito(id_usuario):
    """Obtiene el idPlan de la suscripción activa de un usuario."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT idPlan, fecha_fin, idSuscripcion FROM SUSCRIPCION 
                WHERE idUsuario = %s AND estado = 'A'
                LIMIT 1
            '''
            cursor.execute(query, (id_usuario,))
            result = cursor.fetchone()

            if result:
                id_plan = result[0]
                fecha_fin = result[1]
                id_suscripcion = result[2]

                # Verificar si la suscripción está activa
                return {
                    "idPlan": id_plan,
                    "fecha_fin": fecha_fin,
                    "idSuscripcion": id_suscripcion
                }
            
            else:
                return None
    except Exception as e:
        print(f"[ERROR] Al obtener la suscripción: {e}")
        return None
    finally:
        conexion.close()


def obtener_detalle_local(id):
    """Obtiene los detalles de un local específico."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                SELECT lo.nombre, 
                lo.direccion,
                lo.tel,
                lo.correo
                FROM LOCAL lo
                WHERE lo.idUsuario = %s
            '''
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                return {
                    "nombre": result[0],
                    "direccion": result[1],
                    "tel": result[2],
                    "correo": result[3]
                }
            else:
                return None
    except Exception as e:
        print(f"[ERROR] Al obtener los detalles del local: {e}")
        return None
    
    
def confirmar_suscripcion(idsuscripcion):
    """Confirma la suscripción gratuita."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                UPDATE SUSCRIPCION 
                SET estado = 'A' 
                WHERE idSuscripcion = %s
            '''
            cursor.execute(query, (idsuscripcion,))
            conexion.commit()
            return True
    except Exception as e:
        print(f"[ERROR] Al confirmar la suscripción gratuita: {e}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()
            
def insertar_comprobante_gratuita(igv,subtotal,total,fecha,idSuscripcion):
    """Inserta un comprobante de pago en la base de datos."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                INSERT INTO COMPROBANTE (igv, subtotal, total, fecha, idSuscripcion)
                VALUES (%s, %s, %s, %s, %s)
            '''
            valores = (igv, subtotal, total, fecha, idSuscripcion)
            cursor.execute(query, valores)
            conexion.commit()
            return True
    except Exception as e:
        print(f"[ERROR] Al insertar el comprobante: {e}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()
            
            
def insertar_comprobante_paga(igv, subtotal, total, fecha, idSuscripcion, foto, idFormaPago):
    """Inserta un comprobante de pago en la base de datos."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                INSERT INTO COMPROBANTE (igv, subtotal, total, fecha, idSuscripcion, foto_confirmacion, idFormaPago)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            valores = (igv, subtotal, total, fecha, idSuscripcion, foto, idFormaPago)
            cursor.execute(query, valores)
            conexion.commit()
            return True
    except Exception as e:
        print(f"[ERROR] Al insertar el comprobante: {e}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()


def anular_suscripcion(id):
    """Anula una suscripción."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = '''
                UPDATE SUSCRIPCION 
                SET estado = 'I' 
                WHERE idSuscripcion = %s
            '''
            cursor.execute(query, (id,))
            conexion.commit()
            return True
    except Exception as e:
        print(f"[ERROR] Al anular la suscripción: {e}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()