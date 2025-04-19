import pymysql

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host="shuttle.proxy.rlwy.net",
            port=48036,
            user="root",
            password="eIBwKZTAxcXWewZFzNAfIgmgFAUjRBGN",
            db="CanchasYa"
        )
        return conexion
    except pymysql.MySQLError as e:
        return None
