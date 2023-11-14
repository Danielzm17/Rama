import bom.vista as vistas
import bom.consultas as consultas_bom
import bom_componente.consultas as consultas_bom_componentes
import bom_materia_prima.consultas as consultas_bom_materia_prima
import utils.validaciones as utils_validacion
import utils.ventana as utils_ventana
import producto.consultas as consultas_producto
import materia_prima.consultas as consultas_materia_prima

import PySimpleGUI as psg

from bom.bom import Bom
from bom.consultas import listar_por_sku_nombre
from bom_componente.bom_componente import BomComponente
from bom_materia_prima.bom_materia_prima import BomMateriaPrima


def listar_mensajes_errores_registro():
    # debe corresponder a lista de validación
    return ('Versión es obligatoria y única por producto', 'El comentario es obligatorio',
            'El costo unitario es obligatorio y númerico', 'El costo debe ser mayor o igual a cero')


def validar_condiciones_registro(dato: Bom):
    if dato:
        validacion = (
            not utils_validacion.validar_texto_vacio(dato.version),  # version
            not utils_validacion.validar_texto_vacio(dato.comentario),  # comentario
            utils_validacion.validar_numero_real(dato.costo_operativos),  # costo_unitario
            True if utils_validacion.validar_numero_real(dato.costo_operativos) and float(
                dato.costo_operativos) >= 0 else False
        )
        return validacion
    else:
        return None


def validar_registro(dato: Bom):
    if dato:
        validacion = validar_condiciones_registro(dato)
        return all(validacion)
    else:
        return False


def procesar(
        ventana_actual=None,
        ventana_secundaria=None,
        ventana_auxiliar=None,
        cmd=None,
        valores=None,
        conn=None
):
    ventana = None
    if cmd['evt'] != 'bom':
        psg.popup_error('Intentando procesar un evento de producto, pero se envió otro evento', 'Error de programación')
    else:
        if cmd['det'] == 'main-list':
            if cmd['act'] == 'create':
                ventana = vistas.crear_ventana_registro()
            elif cmd['act'] == 'update':
                nombre_tabla = 'evt:bom;det:list;act:list'
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_secundaria,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    bom = consultas_bom.cargar(conn=conn, id=selected)

                    producto = consultas_producto.cargar(conn=conn, id=bom.producto_id)
                    componentes = consultas_bom_componentes.cargar_componentes(conn=conn, id=bom.bom_id)
                    materias_primas = consultas_bom_materia_prima.cargar_materias_primas(conn=conn, id=bom.bom_id)

                    componentes_productos = [
                        (componente, consultas_producto.cargar(conn=conn, id=componente.componente_id)) for componente
                        in componentes]

                    componentes_materias_primas = [
                        (materia_prima, consultas_materia_prima.cargar(conn=conn, id=materia_prima.materia_prima_id)) for materia_prima
                        in materias_primas]

                    ventana = vistas.crear_ventana_edicion_bom(bom=bom,
                                                               producto=producto,
                                                               componentes=componentes_productos,
                                                               materias_primas=componentes_materias_primas)
                else:
                    psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')
            elif cmd['act'] == 'delete':
                nombre_tabla = 'evt:bom;det:list;act:list'
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_secundaria,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    bom = consultas_bom.cargar(conn=conn, id=selected)
                    productos = consultas_producto.cargar(conn=conn, id=bom.producto_id)

                    ventana = vistas.crear_ventana_bom_eliminar(bom=bom, producto=productos)
                else:
                    psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')
            elif cmd['act'] == 'do-delete':
                bom = valores['bom-id']
                exito, msg, id = consultas_bom.eliminar(conn=conn,
                                                        id=bom)
                if exito:
                    ventana_actual.close()
                    ventana_actual = None
                    datos = [tuple(i for i in l) for l in consultas_bom.cargar_tabla(conn)]
                    ventana_secundaria['evt:bom;det:list;act:list'].update(values=datos)
                    ventana = ventana_secundaria
        elif cmd['det'] == 'add-bom':
            if cmd['act'] == 'prod_find':
                sku = valores['sku']
                nombre = valores['nombre']

                datos = listar_por_sku_nombre(conn=conn, sku=sku, nombre=nombre)

                nombre_tabla = 'evt:bom;det:add-bom;act:prod_list'
                ventana_actual[nombre_tabla].update(values=datos)
                ventana_actual['evt:bom;det:add-bom;act:create'].update(disabled=not bool(datos))
                utils_ventana.centrar_ventana(ventana_actual)
            elif cmd['act'] == 'prod_list':
                nombre_tabla = 'evt:bom;det:add-bom;act:prod_list'
                datos_seleccionados = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_actual,
                                                                                     nombre_tabla=nombre_tabla,
                                                                                     valores=valores)
                if datos_seleccionados:
                    id_seleccionado = int(datos_seleccionados[0][0])
                    bom = consultas_producto.cargar(conn=conn, id=id_seleccionado)
                    ventana_actual['paso03'].update(visible=True)
                    ventana_actual['producto_id'].update(bom.producto_id)
                    ventana_actual['producto_sku'].update(bom.sku)
                    ventana_actual['producto_nombre'].update(bom.nombre)
                    ventana_actual['evt:bom;det:add-bom;act:create'].update(disabled=False)
                else:
                    ventana_actual['evt:bom;det:add-bom;act:create'].update(disabled=True)

            elif cmd['act'] == 'create':
                producto_id = valores['producto_id']
                version = valores['version']
                receta_principal = valores['receta-principal']
                receta_alterna = valores['receta-alterna']
                comentario = valores['comentario']
                costo_operativo = valores['costo-operativo']
                estado_activo = valores['estado-activo']
                estado_inactivo = valores['estado-inactivo']
                duracion_horas = valores['duracion-horas']
                duracion_minutos = valores['duracion-minutos']
                duracion_segundos = valores['duracion-segundos']

                bom = Bom()
                bom.producto_id = producto_id
                bom.version = version
                bom.receta_principal = receta_principal
                bom.comentario = comentario
                bom.costo_operativos = costo_operativo
                bom.estado = 'activo' if estado_activo else 'inactivo'
                bom.tiempo_fabricacion = duracion_horas * 60 + duracion_minutos + duracion_segundos / 60

                if validar_registro(bom):
                    exito, msg, id = consultas_bom.registrar(conn, dato=bom)
                    if exito:
                        ventana_actual.close()
                        ventana_actual = None
                        datos = [tuple(i for i in l) for l in consultas_bom.cargar_tabla(conn)]
                        ventana_secundaria['evt:bom;det:list;act:list'].update(values=datos)
                        ventana = ventana_secundaria
                    else:
                        psg.popup_error(msg, title='Error')
                else:

                    errores = [z[0] for z in
                               zip(listar_mensajes_errores_registro(), validar_condiciones_registro(bom))
                               if
                               not z[1]]
                    psg.popup_error(*errores, title='Revise antes de continuar')
        elif cmd['det'] == 'detail-materia-prima':
            if cmd['act'] == 'add':
                bom = valores['bom-id']
                bom = consultas_bom.cargar(conn=conn, id=bom)
                ventana = vistas.crear_ventana_registro_materia_prima_en_bom(
                    bom=bom)
            elif cmd['act'] == 'update':
                pass
            elif cmd['act'] == 'delete':
                pass
            elif cmd['act'] == 'buscar':
                sku_buscar = valores['sku-buscar']
                nombre_buscar = valores['nombre-buscar']
                tabla = 'evt:{};det:detail-materia-prima;act:select-materia-prima'.format('bom')
                datos = consultas_materia_prima.listar_por_sku_nombre(conn=conn,
                                                                 sku=sku_buscar,
                                                                 nombre=nombre_buscar)

                datos_ajustados = [(dato.materia_prima_id, dato.sku, dato.nombre, dato.unidad) for dato in datos]
                ventana_actual[tabla].update(values=datos_ajustados)
            elif cmd['act'] == 'select-materia-prima':
                nombre_tabla = 'evt:{};det:detail-materia-prima;act:select-materia-prima'.format('bom')
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_actual,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    materias_primas = consultas_materia_prima.cargar(conn=conn, id=selected)
                    ventana_actual['materia-prima-id'].update(materias_primas.materia_prima_id)
                    ventana_actual['sku'].update(materias_primas.sku)
                    ventana_actual['nombre'].update(materias_primas.nombre)

            elif cmd['act'] == 'do-add':
                bom = valores['bom-id']
                materia_prima_id = valores['materia-prima-id']
                cantidad = valores['cantidad']
                unidad = valores['unidad']
                costo_operativo = valores['costo-operativo']
                duracion_horas = valores['duracion-horas']
                duracion_minutos = valores['duracion-minutos']
                duracion_segundos = valores['duracion-segundos']
                print(bom, materia_prima_id, cantidad, unidad, costo_operativo, duracion_horas, duracion_minutos,
                      duracion_segundos)
                bom_materia_prima = BomMateriaPrima()
                bom_materia_prima.bom_id = bom
                bom_materia_prima.materia_prima_id = materia_prima_id
                bom_materia_prima.cantidad = cantidad
                bom_materia_prima.unidad = unidad
                bom_materia_prima.costo_unitario = costo_operativo
                bom_materia_prima.tiempo_fabricacion = (
                                                                duracion_horas * 60 + duracion_minutos + duracion_segundos / 60) / (
                                                                24 * 60)
                bom_materia_prima.tiempo_fabricacion_unidad = 'días'
                exito, msg, id = consultas_bom_materia_prima.registrar(conn=conn, dato=bom_materia_prima)
                print(exito, id, msg)
        elif cmd['det'] == 'detail-componente':
            if cmd['act'] == 'add':
                bom = valores['bom-id']
                bom = consultas_bom.cargar(conn=conn, id=bom)
                productos = consultas_producto.listar_todos(conn=conn)
                ventana = vistas.crear_ventana_registro_componente_en_bom(
                    bom=bom
                )

            elif cmd['act'] == 'update':
                pass
            elif cmd['act'] == 'delete':
                pass
            elif cmd['act'] == 'buscar':
                sku_buscar = valores['sku-buscar']
                nombre_buscar = valores['nombre-buscar']
                tabla = 'evt:{};det:detail-componente;act:select-componente'.format('bom')
                datos = consultas_producto.listar_por_sku_nombre(conn=conn,
                                                                 sku=sku_buscar,
                                                                 nombre=nombre_buscar)

                datos_ajustados = [(dato.producto_id, dato.sku, dato.nombre, dato.unidad) for dato in datos]
                ventana_actual[tabla].update(values=datos_ajustados)
            elif cmd['act'] == 'select-componente':
                nombre_tabla = 'evt:{};det:detail-componente;act:select-componente'.format('bom')
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_actual,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    productos = consultas_producto.cargar(conn=conn, id=selected)
                    ventana_actual['producto-id'].update(productos.producto_id)
                    ventana_actual['sku'].update(productos.sku)
                    ventana_actual['nombre'].update(productos.nombre)

            elif cmd['act'] == 'do-add':
                bom = valores['bom-id']
                producto_id = valores['producto-id']
                cantidad = valores['cantidad']
                unidad = valores['unidad']
                costo_operativo = valores['costo-operativo']
                duracion_horas = valores['duracion-horas']
                duracion_minutos = valores['duracion-minutos']
                duracion_segundos = valores['duracion-segundos']
                print(bom, producto_id, cantidad, unidad, costo_operativo, duracion_horas, duracion_minutos,
                      duracion_segundos)
                bom_materia_prima = BomComponente()
                bom_materia_prima.bom_id = bom
                bom_materia_prima.componente_id = producto_id
                bom_materia_prima.cantidad = cantidad
                bom_materia_prima.unidad = unidad
                bom_materia_prima.costo_unitario = costo_operativo
                bom_materia_prima.tiempo_fabricacion = (
                                                                duracion_horas * 60 + duracion_minutos + duracion_segundos / 60) / (
                                                                24 * 60)
                bom_materia_prima.tiempo_fabricacion_unidad = 'días'
                exito, msg, id = consultas_bom_componentes.registrar(conn=conn, dato=bom_materia_prima)
                print(exito, id, msg)

    return ventana
