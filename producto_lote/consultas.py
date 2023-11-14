import sqlite3
from typing import Dict, List, Any

from producto_lote.producto_lote import Producto_lote


def registrar(conn=None, dato: Producto_lote = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO producto_lote 
        (
            sku,
            nombre,
            costo,
            precio,
            cantidad,
            dias_vida_util
        )
        VALUES
        (
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

        valores = (dato.sku, dato.nombre, dato.costo, dato.precio, dato.cantidad, dato.dias_vida_util)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn=None, dato: Producto_lote = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update producto_lote 
        set
            sku = ?,
            nombre = ?,
            costo = ?,
            precio = ?,
            cantidad = ?,
            dias_vida_util = ?
        where
            producto_lote_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.sku, dato.nombre, dato.costo, dato.precio, dato.cantidad, dato.dias_vida_util)

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
        delete from producto_lote 
        where producto_lote_id = ?;
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
        dato.sku, dato.nombre, dato.costo, dato.precio, dato.cantidad, dato.dias_vida_util) for dato in listado]

    return salida


def listar_todos(conn=None) -> List[Producto_lote]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        producto_lote_id,
        sku,
        nombre,
        fecha_registro,
        costo,
        precio,
        cantidad,
        dias_vida_util
    from 
        producto_lote
    ''').fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida

def listar_por_sku_nombre(conn, sku, nombre) -> List[Producto_lote]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        producto_lote_id,
        sku,
        nombre,
        fecha_registro,
        costo,
        precio,
        cantidad,
        dias_vida_util
    from 
        producto_lote
    where
        sku like '%{}%'
        and
        nombre like '%{}%'
    '''.format(sku,nombre)).fetchall()

    for resultado in resultados:
        salida.append(convertir_dict_en_objeto(convertir_row_en_dict(resultado)))

    return salida



def cargar(conn=None, id=-1) -> Producto_lote:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        producto_lote_id,
        sku,
        nombre,
        fecha_registro,
        costo,
        precio,
        cantidad,
        dias_vida_util
    from 
        producto_lote
    where
        producto_lote_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))


def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos: Dict) -> Producto_lote:
    objeto = Producto_lote()
    objeto.producto_lote_id = datos['producto_lote_id']
    objeto.sku = datos['sku']
    objeto.nombre = datos['nombre']
    objeto.fecha_registro = datos['fecha_registro']
    objeto.costo = datos['costo']
    objeto.precio = datos['precio']
    objeto.cantidad = datos['cantidad']
    objeto.dias_vida_util = datos['dias_vida_util']
    return objeto
