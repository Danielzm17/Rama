import sqlite3
from typing import Dict, List, Any, Tuple

from bom_componente.bom_componente import BomComponente


def registrar(conn, dato: BomComponente) -> Tuple[bool, str, int]:
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO bom_componente 
        (
            bom_id,
            componente_id,
            cantidad,
            unidad,
            costo_unitario,
            tiempo_fabricacion,
            tiempo_fabricacion_unidad
        )
        VALUES
        (
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

        valores = (dato.bom_id, dato.componente_id, dato.cantidad,
                   dato.unidad, dato.costo_unitario, dato.tiempo_fabricacion,
                   dato.tiempo_fabricacion_unidad)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn, dato: BomComponente):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update bom_componente 
        set
            bom_id = ?,
            componente_id = ?,
            cantidad = ?,
            unidad = ?,
            costo_unitario = ?,
            tiempo_fabricacion = ?,
            tiempo_fabricacion_unidad = ?
        where
            bom_componente_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.bom_id, dato.componente_id, dato.cantidad,
                   dato.unidad, dato.costo_unitario, dato.tiempo_fabricacion,
                   dato.tiempo_fabricacion_unidad, dato.bom_componente_id)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def eliminar(conn, id: int):
    exito = True
    msg = 'Operación exitosa'
    # id = -1
    sql = '''
        delete from bom_componente 
        where bom_id = ?;
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


def listar_todos(conn) -> List[BomComponente]:
    salida = []
    # conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
        SELECT
            bom_componente_id,
            bom_id,
            componente_id,
            cantidad,
            unidad,
            costo_unitario,
            tiempo_fabricacion,
            tiempo_fabricacion_unidad
        FROM
            bom_componente
    ''').fetchall()

    return salida

def cargar_componentes(conn, id:int):
    resultado = conn.execute('''
SELECT
    bom_componente_id,
    bom_id,
    componente_id,
    cantidad,
    unidad,
    costo_unitario,
    tiempo_fabricacion,
    tiempo_fabricacion_unidad
FROM
    bom_componente
WHERE
    bom_id = ?
    ''', (id,)).fetchall()

    salida = [convertir_dict_en_objeto(convertir_row_en_dict(r)) for r in resultado]

    return salida


def cargar(conn, id: int) -> BomComponente:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        bom_componente_id,
        bom_id,
        componente_id,
        cantidad,
        unidad,
        costo_unitario,
        tiempo_fabricacion,
        tiempo_fabricacion_unidad
    from 
        bom_componente
    where
        bom_componente_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))


def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos: Dict) -> BomComponente:
    objeto = BomComponente()
    objeto.bom_componente_id = datos['bom_componente_id']
    objeto.bom_id = datos['bom_id']
    objeto.componente_id = datos['componente_id']
    objeto.cantidad = datos['cantidad']
    objeto.unidad = datos['unidad']
    objeto.costo_unitario = datos['costo_unitario']
    objeto.tiempo_fabricacion = datos['tiempo_fabricacion']
    objeto.tiempo_fabricacion_unidad = datos['tiempo_fabricacion_unidad']
    return objeto
