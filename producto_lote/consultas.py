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
            costo_unitario,
            porcentaje_impuesto,
            monto_impuesto,
            monto_utilidad,
            precio,
            redondeo,
            precio_final,
            cantidad,
            unidad,
            disponible,
            reservado,
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

        valores = (dato.sku, dato.nombre, dato.costo_unitario, dato.porcentaje_impuesto, dato.monto_impuesto,
                   dato.monto_utilidad, dato.precio, dato.redondeo, dato.precio_final, dato.cantidad,
                   dato.unidad, dato.disponible, dato.reservado, dato.estado, dato.dias_vida_util)

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
            costo_unitario = ?,
            porcentaje_impuesto = ?,
            monto_impuesto = ?,
            monto_utilidad = ?,
            precio = ?,
            redondeo = ?,
            precio_final = ?,
            cantidad = ?,
            unidad = ?,
            disponible = ?,
            reservado = ?,
            estado = ?,
            dias_vida_util = ?
        where
            producto_lote_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.sku, dato.nombre, dato.costo_unitario, dato.porcentaje_impuesto, dato.monto_impuesto,
                   dato.monto_utilidad, dato.precio, dato.redondeo, dato.precio_final, dato.cantidad,
                   dato.unidad, dato.disponible, dato.reservado, dato.estado, dato.dias_vida_util,dato.producto_lote_id)

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
        dato.producto_lote_id, dato.sku, dato.nombre, dato.cantidad, dato.disponible, dato.reservado, dato.unidad,
        dato.costo_unitario, dato.estado, dato.dias_vida_util) for dato in listado]

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
        costo_unitario,
        porcentaje_impuesto,
        monto_impuesto,
        monto_utilidad,
        precio,
        redondeo,
        precio_final,
        cantidad,
        unidad,
        disponible,
        reservado,
        estado,
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
        costo_unitario,
        porcentaje_impuesto,
        monto_impuesto,
        monto_utilidad,
        precio,
        redondeo,
        precio_final,
        cantidad,
        unidad,
        disponible,
        reservado,
        estado,
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
        costo_unitario,
        porcentaje_impuesto,
        monto_impuesto,
        monto_utilidad,
        precio,
        redondeo,
        precio_final,
        cantidad,
        unidad,
        disponible,
        reservado,
        estado,
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
    objeto.costo_unitario = datos['costo_unitario']
    objeto.porcentaje_impuesto = datos['porcentaje_impuesto']
    objeto.monto_impuesto = datos['monto_impuesto']
    objeto.monto_utilidad = datos['monto_utilidad']
    objeto.precio = datos['precio']
    objeto.redondeo = datos['redondeo']
    objeto.precio_final = datos['precio_final']
    objeto.cantidad = datos['cantidad']
    objeto.unidad = datos['unidad']
    objeto.disponible = datos['disponible']
    objeto.reservado = datos['reservado']
    objeto.estado = datos['estado']
    objeto.dias_vida_util = datos['dias_vida_util']
    return objeto
