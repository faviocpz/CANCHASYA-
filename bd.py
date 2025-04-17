import pymysql

def obtener_conexion():
   return pymysql.connect(host='shuttle.proxy.rlwy.net',
                           user='root',                           
                           password='eIBwKZTAxcXWewZFzNAfIgmgFAUjRBGN',
                          db='CanchasYa',
                          port=48036)

