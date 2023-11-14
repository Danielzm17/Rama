import sqlite3
from typing import Dict, List, Any

from bom_materia_prima.bom_materia_prima import BomMateriaPrima


def registrar(conn, dato: BomMateriaPrima):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO bom_materia_prima 
        (
            bom_id,
            materia_prima_id,
            cantidad,
            unidad,
            costo,
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

        valores = (dato.bom_id, dato.materia_prima_id, dato.cantidad,
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


def modificar(conn, dato: BomMateriaPrima):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update bom_materia_prima 
        set
            bom_id = ?,
            materia_prima_id = ?,
            cantidad = ?,
            unidad = ?,
            costo = ?,
            tiempo_fabricacion = ?,
            tiempo_fabricacion_unidad = ?
        where
            bom_componente_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.bom_id, dato.materia_prima_id, dato.cantidad,
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
        delete from bom_materia_prima 
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


def listar_todos(conn) -> List[BomMateriaPrima]:
    salida = []
    # conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
        SELECT
            bom_componente_id,
            bom_id,
            materia_prima_id,
            cantidad,
            unidad,
            costo,
            tiempo_fabricacion,
            tiempo_fabricacion_unidad
        FROM
            bom_materia_prima
    ''').fetchall()

    return salida


def cargar(conn, id: int) -> BomMateriaPrima:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        bom_componente_id,
        bom_id,
        materia_prima_id,
        cantidad,
        unidad,
        costo,
        tiempo_fabricacion,
        tiempo_fabricacion_unidad
    from 
        bom_materia_prima
    where
        bom_componente_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))


def cargar_materias_primas(conn, id:int):
    resultado = conn.execute('''
SELECT
    bom_materia_prima_id,
    bom_id,
    materia_prima_id,
    cantidad,
    unidad,
    costo,
    tiempo_fabricacion,
    tiempo_fabricacion_unidad
FROM
    bom_materia_prima
WHERE
    bom_id = ?
    ''', (id,)).fetchall()

    salida = [convertir_dict_en_objeto(convertir_row_en_dict(r)) for r in resultado]

    return salida


def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos: Dict) -> BomMateriaPrima:
    objeto = BomMateriaPrima()
    objeto.bom_materia_prima_id = datos['bom_materia_prima_id']
    objeto.materia_prima_id = datos['materia_prima_id']
    objeto.bom_id = datos['bom_id']
    objeto.cantidad = datos['cantidad']
    objeto.unidad = datos['unidad']
    objeto.costo_unitario = datos['costo']
    objeto.tiempo_fabricacion = datos['tiempo_fabricacion']
    objeto.tiempo_fabricacion_unidad = datos['tiempo_fabricacion_unidad']
    return objeto
