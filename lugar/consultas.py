import sqlite3
from typing import Dict, List, Any

from lugar.lugar import Local


def registrar(conn, dato: Local):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO lugar 
        (
            nombre,
            estado
        )
        VALUES
        (
            ?,
            ?
        );
    '''

    cursor = conn.cursor()
    try:

        valores = (dato.nombre, dato.estado)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn, dato:Local):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update lugar 
        set
            nombre = ?,
            estado = ?
        where
            lugar_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.nombre, dato.estado, dato.lugar_id)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def eliminar(conn, id):
    exito = True
    msg = 'Operación exitosa'
    # id = -1
    sql = '''
        delete from lugar 
        where lugar_id = ?;
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


def cargar_tabla(conn):
    listado = listar_todos(conn=conn)
    salida = []

    filtro = lambda dato: dato.estado == 'activo' or dato.estado == 'inactivo'
    ordenar = lambda dato: dato.nombre

    listado.sort(key=ordenar)
    listado = list(filter(filtro, listado))

    salida = [(dato.lugar_id,dato.nombre, dato.estado) for dato in listado]

    return salida


def listar_todos(conn) -> List[Local]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        lugar_id,
        nombre,
        estado
    from 
        lugar
    ''').fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida


def cargar(conn, id) -> Local:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        lugar_id,
        nombre,
        estado
    from 
        lugar
    where
        lugar_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))

def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos:Dict) ->Local:
    objeto = Local()
    objeto.lugar_id = datos['lugar_id']
    objeto.nombre = datos['nombre']
    objeto.estado = datos['estado']
    return objeto
