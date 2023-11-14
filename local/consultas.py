import sqlite3
from typing import Dict, List, Any

from local.local import Local


def registrar(conn=None, dato: Local = None):
    #print(dato.nombre)
    #print(dato.local_id)
    print("hols")
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO local 
        (
            nombre,
            estado,
            lugar_id


        )
        VALUES
        (
            ?,
            ?,
            ?

  
        );
    '''

    cursor = conn.cursor()
    try:

        valores = [dato.nombre, dato.estado, dato.lugar_id]
        print("es execute")
        cursor.execute(sql, valores)
        print("es commit")
        conn.commit()

    except sqlite3.IntegrityError as e:
        print("ERROR")
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn=None, dato: Local = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update local 
        set
            nombre = ?,
            estado = ?,
            lugar_id = ?
            
        where
            local_id = ?;  

    '''

    cursor = conn.cursor()
    try:
        valores = (dato.nombre, dato.estado, dato.lugar_id, dato.local_id)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def eliminar(conn=None, id=None):
    exito = True
    msg = 'Operación exitosa'
    # id = -1
    sql = '''
        delete from local 
        where local_id = ?;
    '''

    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id,))
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    #  id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def cargar_tabla(conn=None):
    listado = listar_todos(conn=conn)
    salida = []

    filtro = lambda dato: dato.estado == 'activo' or dato.estado == 'inactivo'
    ordenar = lambda dato: dato.nombre

    listado.sort(key=ordenar)
    listado = list(filter(filtro, listado))

    salida = [(
        dato.local_id, dato.nombre, dato.estado, dato.lugar_id) for dato in listado]

    return salida


def listar_todos(conn=None) -> List[Local]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        local_id,
        nombre,
        estado,
        lugar_id
    from 
        local
    ''').fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida

def listar_por_id_nombre(conn, local_id, nombre) -> List[Local]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        local_id,
        nombre,
        estado,
        lugar_id
    from 
        local
    where
        local_id like '%{}%'
        and
        nombre like '%{}%'
    '''.format(local_id, nombre)).fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida



def cargar(conn=None, id=-1) -> Local:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        local_id,
        nombre,
        estado,
        lugar_id
    from 
        local
    where
        local_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))


def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos: Dict) -> Local:
    objeto = Local()
    objeto.local_id = datos['local_id']
    objeto.nombre = datos['nombre']
    objeto.estado = datos['estado']
    objeto.lugar_id = datos['lugar_id']
    return objeto
