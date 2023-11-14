import sqlite3
from typing import Dict, List, Any

from bom.bom import Bom


def registrar(conn=None, dato: Bom = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO bom 
        (
            producto_id,
            version,
            receta_principal,
            comentario,
            costo_acumulado_componentes,
            costo_acumulado_materia_prima,
            costo_operativos,
            costo_total,
            tiempo_fabricacion,
            fecha_registro,
            estado
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
            ?
        );
    '''

    cursor = conn.cursor()
    try:

        valores = (dato.producto_id, dato.version, dato.receta_principal, dato.comentario,
                   dato.costo_acumulado_componentes, dato.costo_acumulado_materia_prima, dato.costo_operativos,
                   dato.costo_total, dato.tiempo_fabricacion, dato.fecha_registro, dato.estado)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn=None, dato: Bom = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update bom 
        set
            producto_id,
            version,
            receta_principal,
            comentario,
            costo_acumulado_componentes,
            costo_acumulado_materia_prima,
            costo_operativos,
            costo_total,
            tiempo_fabricacion,
            fecha_registro,
            estado
        where
            bom_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.producto_id, dato.version, dato.receta_principal, dato.comentario,
                   dato.costo_acumulado_componentes, dato.costo_acumulado_materia_prima, dato.costo_operativos,
                   dato.costo_total, dato.tiempo_fabricacion, dato.fecha_registro, dato.estado, dato.bom_id)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def eliminar(conn, id:int):
    exito = True
    msg = 'Operación exitosa'
    # id = -1
    sql = '''
        delete from bom 
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


def cargar_tabla(conn=None):
    resultados = conn.execute('''
    SELECT
        b.bom_id,
        p.sku,
        p.nombre,
        b.version,
        CASE b.receta_principal
        WHEN 1 THEN 'Receta principal'
        WHEN 0 THEN 'Receta alterna'
        END,
        b.estado,
        b.costo_acumulado_componentes,
        b.costo_acumulado_materia_prima,
        b.costo_operativos
    FROM
        bom as b
    JOIN
        producto as p
        on b.producto_id = p.producto_id
    WHERE
        b.estado in ('activo','inactivo')
    ORDER BY
        p.nombre,
        b.receta_principal DESC,
        b.estado
        ''').fetchall()

    # salida = []
    # for resultado in resultados:
    #
    #     salida.append((resultado[0],resultado[1]))
    # for resultado in resultados:
    #     salida.append(convertirDictEnObjeto(convertirRowEnDict(resultado)))

    return resultados


def listar_todos(conn=None) -> List[Bom]:
    salida = []
    # conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
SELECT
    b.bom_id,
    p.sku,
    p.nombre,
    b.version,
    CASE b.receta_principal
    WHEN 1 THEN 'Receta principal'
    WHEN 0 THEN 'Receta alterna'
    END,
    b.estado,
    b.costo_acumulado_componentes,
    b.costo_acumulado_materia_prima,
    b.costo_operativos
FROM
    bom as b
JOIN
    producto as p
    on b.producto_id = p.producto_id
WHERE
    b.estado in ('activo','inactivo')
ORDER BY
    p.nombre,
    b.receta_principal DESC,
    b.estado
    ''').fetchall()

    # for resultado in resultados:
    #     salida.append(convertirDictEnObjeto(convertirRowEnDict(resultado)))

    return salida

def listar_por_sku_nombre(conn=None, sku=None, nombre=None):
    if sku is None:
        sku = ''
    if nombre is None:
        nombre = ''
    sku = f'%{sku}%'
    nombre = f'%{nombre}%'
    resultados = conn.execute('''
SELECT
    p.producto_id,
    p.sku,
    p.nombre,
    p.estado
FROM
    producto as p
WHERE
    p.sku like ?
    AND
    p.nombre like ?
    AND
    estado in ('activo', 'inactivo')
    ''', (sku, nombre)).fetchall()

    return resultados

def cargar(conn=None, id=-1) -> Bom:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        bom_id,
        producto_id,
        version,
        receta_principal,
        comentario,
        costo_acumulado_componentes,
        costo_acumulado_materia_prima,
        costo_operativos,
        costo_total,
        tiempo_fabricacion,
        fecha_registro,
        estado
    from 
        bom
    where
        bom_id = ?
    ''', (id,)).fetchone()

    return convertir_dict_en_objeto(convertir_row_en_dict(resultado))




def cargar_materias_primas(conn, dato:Bom):
    resultado = conn.execute('''
SELECT
      bmp.bom_materia_prima_id
    , bmp.bom_id
    , bmp.materia_prima_id
    , mp.nombre as materia_prima_nombre
    , bmp.cantidad
    , bmp.unidad
    , bmp.costo
    , bmp.tiempo_fabricacion
    , bmp.tiempo_fabricacion_unidad
FROM
    bom_materia_prima as bmp
JOIN
    materia_prima as mp
    on bmp.materia_prima_id = mp.materia_prima_id
WHERE
    bmp.bom_id = ?
    ''', (dato.bom_id,)).fetchall()

    return resultado

def listar_otros_componentes_bom(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
     p.producto_id
    ,p.sku
    ,p.nombre
FROM
    producto as p
WHERE
    p.producto_id not in (
    SELECT
        bc.componente_id
    FROM
        bom_componente as bc
    WHERE
        bc.bom_id = ?
    )
    AND
    p.estado = 'activo'
ORDER BY
    p.nombre
    ''', (id,)).fetchall()

    return resultado


def listar_otras_materias_primas_bom(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
     mp.materia_prima_id
    ,mp.sku
    ,mp.nombre
FROM
    materia_prima as  mp
WHERE
    mp.materia_prima_id not in (
    SELECT
        bmp.bom_materias_primas_id
    FROM
        bom_materia_prima as bmp
    WHERE
        bmp.bom_id = 1
    )
    AND
    mp.estado = 'activo'
ORDER BY
    mp.nombre
    ''', (id,)).fetchall()

    salida = [ convertir_row_en_dict(fila) for fila in resultado]

    return resultado


def convertir_row_en_dict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertir_dict_en_objeto(datos:Dict) -> Bom:
    objeto = Bom()
    objeto.bom_id = datos['bom_id']
    objeto.producto_id = datos['producto_id']
    objeto.version = datos['version']
    objeto.receta_principal = datos['receta_principal']
    objeto.comentario = datos['comentario']
    objeto.costo_acumulado_componentes = datos['costo_acumulado_componentes']
    objeto.costo_acumulado_materia_prima = datos['costo_acumulado_materia_prima']
    objeto.costo_operativos = datos['costo_operativos']
    objeto.costo_total = datos['costo_total']
    objeto.tiempo_fabricacion = datos['tiempo_fabricacion']
    objeto.fecha_registro = datos['fecha_registro']
    objeto.estado = datos['estado']
    return objeto
