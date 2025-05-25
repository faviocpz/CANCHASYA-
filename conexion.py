import pymysql

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host="metro.proxy.rlwy.net",
            port=48170,
            user="root",
            password="ADspxDQchOVQAknDNlcPyJfzYgSQptEO",
            db="CanchasYa"
        )
        return conexion
    except pymysql.MySQLError as e:
        return None
