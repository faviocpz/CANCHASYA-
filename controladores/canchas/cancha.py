from conexion import obtener_conexion

def consultar_cancha(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """
            select c.descripcion, c.preciom, c.preciot, c.precion, c.puntuacion, c.estado,idDeporte
            from CANCHA c 
            where c.idCancha = %s
            """
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                cancha = {
                    "descripcion": result[0],
                    "precio_manana": result[1],
                    "precio_tarde": result[2],
                    "precio_noche": result[3],
                    "puntuacion": result[4],
                    "estado": result[5],
                    "idDeporte": result[6]
                }
                return cancha
            else:
                return None
    finally:
        conexion.close()
        
def consultar_fotos(id_cancha):
    sql = """
    SELECT
      fo.nombre,
      fo.foto
    FROM FOTO AS fo
    WHERE fo.idCancha = %s
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, (id_cancha,))
            filas = cursor.fetchall()
        fotos = []
        for nombre, foto in filas:
            fotos.append({
                "nombre": nombre,
                "foto":   foto
            })
        return fotos
    finally:
        conexion.close()
        
def consultar_cancha_x_persona(id_usuario):
    sql = """
        SELECT
            ca.idCancha,
            ca.descripcion,
            ca.preciom,
            ca.preciot,
            ca.precion,
            ca.estado,
            GROUP_CONCAT(fo.foto SEPARATOR ',') AS fotos
        FROM CANCHA AS ca
        INNER JOIN LOCAL AS lo ON lo.idLocal = ca.idLocal
        LEFT JOIN FOTO AS fo ON fo.idCancha = ca.idCancha
        WHERE lo.idUsuario = %s
        GROUP BY
            ca.idCancha,
            ca.descripcion,
            ca.preciom,
            ca.preciot,
            ca.precion,
            ca.estado
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, (id_usuario,))
            filas = cursor.fetchall()
        canchas = []
        for idCancha, descripcion, preciom, preciot, precion, estado, fotos_csv in filas:
            fotos = fotos_csv.split(',') if fotos_csv else []
            canchas.append({
                "idCancha":    idCancha,
                "descripcion": descripcion,
                "precio":      preciom,
                "precio_t":    preciot,
                "precio_n":    precion,
                "estado":      estado,
                "fotos":       fotos
            })
        return canchas
    finally:
        conexion.close()



def consultar_detalle_cancha(id_cancha):
    sql = """
    SELECT
      ca.idCancha,
      ca.descripcion,
      ca.preciom,
      ca.preciot,
      ca.precion,
      ca.estado,
      de.nombre AS deporte,
      GROUP_CONCAT(DISTINCT fo.foto
                   ORDER BY fo.idFoto
                   SEPARATOR ',') AS fotos_csv
    FROM CANCHA AS ca
    JOIN LOCAL AS lo ON lo.idLocal = ca.idLocal
    JOIN DEPORTE AS de ON de.idDeporte = ca.idDeporte
    LEFT JOIN FOTO AS fo ON fo.idCancha = ca.idCancha
    WHERE ca.idCancha = %s
    GROUP BY
      ca.idCancha,
      ca.descripcion,
      ca.preciom,
      ca.preciot,
      ca.precion,
      ca.estado,
      de.nombre;
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id_cancha,))
            row = cur.fetchone()
            if not row:
                return None

            (idC, desc, preciom, preciot, precion, estado, deporte, fotos_csv) = row
            
            return {
                "idCancha":    idC,
                "descripcion": desc,
                "preciom":     float(preciom),
                "preciot":     float(preciot),
                "precion":     float(precion),
                "estado":      estado,
                "deporte":     deporte,
                "fotos":       fotos_csv.split(',') if fotos_csv else []
            }
    finally:
        conn.close()




def tipo_cancha():
    sql = """
    SELECT de.idDeporte, de.nombre FROM DEPORTE de WHERE de.estado = 'A'
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql)
            filas = cursor.fetchall()
        tipos = []
        for idDeporte, nombre in filas:
            tipos.append({
                "idTipoCancha": idDeporte,
                "nombre":       nombre
            })
        return tipos
    finally:
        conexion.close()
        
def id_local(id_usuario):
    sql = """
    SELECT lo.idLocal FROM LOCAL lo WHERE lo.idUsuario = %s
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, (id_usuario,))
            id_local = cursor.fetchone()
        return id_local[0] if id_local else None
    finally:
        conexion.close()
        


def insertar_cancha(descripcion, preciom, preciot, precion, puntuacion, id_local, id_deporte):
    sql = """
      INSERT INTO CANCHA
        (descripcion, preciom, preciot, precion, puntuacion, estado, idLocal, idDeporte)
      VALUES
        (%s, %s, %s, %s, %s, 'A', %s, %s)
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (descripcion, preciom, preciot, precion, puntuacion, id_local, id_deporte))
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()


def insertar_horario(id_cancha, dias, h_inicio, h_fin, estado='A'):
    """
    Inserta UN registro en HORARIO,
    guardando la lista de días como texto en `dias`.
    """
    sql = """
      INSERT INTO HORARIO
        (dias, h_inicio, h_fin, estado, idCancha)
      VALUES
        (%s,   %s,       %s,    %s,     %s)
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (dias, h_inicio, h_fin, estado, id_cancha))
            conn.commit()
    finally:
        conn.close()

def insertar_foto(id_cancha, nombre, ruta):
    """
    Inserta un registro en FOTO apuntando al archivo guardado.
    """
    sql = """
      INSERT INTO FOTO
        (nombre, foto, idCancha)
      VALUES
        (%s,     %s,   %s)
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (nombre, ruta, id_cancha))
            conn.commit()
    finally:
        conn.close()

def listar_canchas_idalquilador(id,fecha):
    try:
        conexion = obtener_conexion()
        lista_cancha = []

        with conexion.cursor() as cursor:
            sql = '''
                select idCancha,descripcion from CANCHA as ch
                    where ch.idLocal =  (select lc.idLocal from LOCAL as lc where lc.idUsuario = %s) and ch.estado = 'A';
            '''
            cursor.execute(sql,(id))
            canchas = cursor.fetchall()
            sql2= '''
                select * from RESERVA
                    where fecha = %s
                ORDER BY idCancha ;
                '''
            cursor.execute(sql2, fecha)
            reservas = cursor.fetchall()

            for cancha in canchas:
                print(canchas)
                lista_reserva = []
                dt_cancha = {
                    'id_cancha': cancha[0],
                    'nombre': cancha[1],
                    'fecha': fecha,
                    'reservas': []
                }

                for reserva in reservas:
                    print(reserva)
                    if reserva[4] == cancha[0]:
                        dt_cancha['reservas'].append(str(reserva[2]))
                    

                lista_cancha.append(dt_cancha)
            print(lista_cancha)
            sql3 = '''
                SELECT ha.* FROM LOCAL as lc INNER JOIN HORARIO_ATENCION as ha
                    on ha.idLocal = lc.idLocal
                where lc.idUsuario = %s  
            '''
            cursor.execute(sql3,(id))
            horario = cursor.fetchone()
            return lista_cancha, horario if lista_cancha else None
    except:
        return None
    finally:
        conexion.close()  




def modificar_cancha(id, descripcion, preciom, preciot, precion, puntuacion, estado):
    sql = """
      UPDATE CANCHA
      SET
        descripcion = %s,
        preciom     = %s,
        preciot     = %s,
        precion     = %s,
        puntuacion  = %s,
        estado      = %s
      WHERE idCancha = %s
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (descripcion, preciom, preciot, precion, puntuacion, estado, id))
            conn.commit()
    finally:
        conn.close()
        
def eliminar_foto(id):
    sql = """
      DELETE FROM FOTO
      WHERE idCancha = %s
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (id,))
            conn.commit()
    finally:
        conn.close()