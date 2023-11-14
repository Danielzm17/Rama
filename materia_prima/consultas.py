import sqlite3
from typing import Dict, List, Any

from materia_prima.materia_prima import MateriaPrima


def registrar(conn=None, dato: MateriaPrima = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO materia_prima 
        (
            sku,
            nombre,
            cantidad,
            unidad,
            disponible,
            reservado,
            costo_unitario,
            estado,
            dias_vida_util
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
    '''

    cursor = conn.cursor()
    try:

        valores = (dato.sku, dato.nombre,dato.cantidad, dato.unidad, dato.disponible, dato.reservado, dato.costo_unitario, dato.estado, dato.dias_vida_util)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn=None, dato: MateriaPrima = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update materia_prima 
        set
            sku = ?,
            nombre = ?,
            cantidad = ?,
            unidad = ?,
            disponible = ?,
            reservado = ?,
            costo_unitario = ?,
            estado = ?,
            dias_vida_util = ?
        where
            materia_prima_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (
        dato.sku, dato.nombre, dato.cantidad, dato.unidad, dato.disponible, dato.reservado, dato.costo_unitario,
        dato.estado, dato.dias_vida_util, dato.materia_prima_id)

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
        delete from materia_prima 
        where materia_prima_id = ?;
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
        dato.materia_prima_id, dato.sku, dato.nombre, dato.cantidad, dato.disponible, dato.reservado, dato.unidad,
        dato.costo_unitario, dato.estado, dato.dias_vida_util) for dato in listado]

    return salida


def listar_todos(conn=None) -> List[MateriaPrima]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        materia_prima_id,
        sku,
        nombre,
        fecha_registro,
        unidad,
        costo_unitario,
        cantidad,
        disponible,
        reservado,
        estado,
        dias_vida_util
    from 
        materia_prima
    ''').fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida


def cargar(conn=None, id=-1) -> MateriaPrima:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        materia_prima_id,
        sku,
        nombre,
        fecha_registro,
        unidad,
        costo_unitario,
        cantidad,
        disponible,
        reservado,
        estado,
        dias_vida_util
    from 
        materia_prima
    where
        materia_prima_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))


def listar_por_sku_nombre(conn, sku, nombre) -> List[MateriaPrima]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        materia_prima_id,
        sku,
        nombre,
        fecha_registro,
        unidad,
        costo_unitario,
        cantidad,
        disponible,
        reservado,
        estado,
        dias_vida_util
    from 
        materia_prima
    where
        sku like '%{}%'
        and
        nombre like '%{}%'
    '''.format(sku,nombre)).fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida


def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos:Dict) ->MateriaPrima:
    objeto = MateriaPrima()
    objeto.materia_prima_id = datos['materia_prima_id']
    objeto.sku = datos['sku']
    objeto.nombre = datos['nombre']
    objeto.fecha_registro = datos['fecha_registro']
    objeto.unidad = datos['unidad']
    objeto.costo_unitario = datos['costo_unitario']
    objeto.cantidad = datos['cantidad']
    objeto.disponible = datos['disponible']
    objeto.reservado = datos['reservado']
    objeto.estado = datos['estado']
    objeto.dias_vida_util = datos['dias_vida_util']
    return objeto
