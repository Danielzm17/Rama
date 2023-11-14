from typing import Tuple, Optional
import producto_lote.vista as vistas
import producto_lote.consultas as consultas
import utils.validaciones as utils_validacion
import utils.ventana as utils_ventana
import PySimpleGUI as psg

from producto_lote.producto_lote import Producto_lote


def obtener_alias_controlador() -> str:
    return 'producto_lote'


def listar_mensajes_errores_actualizacion() -> Tuple[str, ...]:
    # debe corresponder a lista de validación
    return ('Revise SKU',
            'Revise el nombre',
            'Revise la cantidad',
            'Revise la unidad',
            'Revise el costo unitario',
            'Revise el estado')


def validar_condiciones_actualizacion(dato: Producto_lote):
    if dato:
        # tiene que coincidir con el orden y cantidad de los mensajes en def listar_mensajes_errores_actualizacion()
        validacion = (
            not utils_validacion.validar_texto_vacio(dato.sku),
            not utils_validacion.validar_texto_vacio(dato.nombre),
            utils_validacion.validar_numero_real(dato.cantidad),
            not utils_validacion.validar_texto_vacio(dato.unidad),
            utils_validacion.validar_numero_real(dato.costo_unitario),
            not utils_validacion.validar_texto_vacio(dato.estado)
        )
        return validacion
    else:
        return ()


def validar_actualizacion(dato: Producto_lote) -> bool:
    if dato:
        validacion = validar_condiciones_creacion(dato)
        return all(validacion)
    else:
        return False


def listar_mensajes_errores_creacion() -> Tuple[str, ...]:
    # debe corresponder a lista de validación
    return ('Revise SKU',
            'Revise el nombre',
            'Revise la cantidad',
            'Revise la unidad',
            'Revise el precio',
            'Revise el costo unitario',
            'Revise el estado')


def validar_condiciones_creacion(dato: Producto_lote) -> Optional[Tuple[bool, ...]]:
    if dato:
        validacion = (
            not utils_validacion.validar_texto_vacio(dato.sku),
            not utils_validacion.validar_texto_vacio(dato.nombre),
            utils_validacion.validar_numero_real(dato.cantidad),
            not utils_validacion.validar_texto_vacio(dato.unidad),
            utils_validacion.validar_numero_real(dato.disponible),
            utils_validacion.validar_numero_real(dato.reservado),
            utils_validacion.validar_numero_real(dato.costo_unitario),
            not utils_validacion.validar_texto_vacio(dato.estado),
            utils_validacion.validar_numero_real(dato.dias_vida_util)
        )
        return validacion
    else:
        return None


def validar_creacion(dato: Producto_lote) -> bool:
    if dato:
        validacion = validar_condiciones_creacion(dato)
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
    if cmd['evt'] != obtener_alias_controlador():
        psg.popup_error('Intentando procesar un evento de producto, pero se envió otro evento', 'Error de programación')
    else:
        if cmd['det'] == 'list':
            if cmd['act'] == 'create':
                ventana = vistas.crear_ventana_registro()
            elif cmd['act'] == 'update':
                nombre_tabla = 'evt:{};det:list;act:list'.format(obtener_alias_controlador())
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_secundaria,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    dato: Producto_lote = consultas.cargar(conn=conn, id=selected)
                    ventana = vistas.crear_ventana_actualizacion(dato)
                else:
                    psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')
            elif cmd['act'] == 'delete':
                nombre_tabla = 'evt:{};det:list;act:list'.format(obtener_alias_controlador())
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_secundaria,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    dato: Producto_lote = consultas.cargar(conn=conn, id=selected)
                    ventana = vistas.crear_ventana_eliminacion(dato)
                else:
                    psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')
        elif cmd['det'] == 'create':
            if cmd['act'] == 'ok':
                producto = Producto_lote()
                producto.sku = valores['sku']
                producto.nombre = valores['nombre']
                producto.unidad = valores['unidad']
                producto.costo_unitario = valores['costo-unitario']
                producto.cantidad = valores['cantidad']
                producto.disponible = valores['disponible']
                producto.reservado = valores['reservado']
                producto.dias_vida_util = valores['dias-vida-util']
                producto.porcentaje_impuesto = valores['porcentaje-impuesto']
                producto.monto_utilidad = valores['monto_utilidad']
                producto.precio = valores['precio']
                producto.redondeo = valores['redondeo']
                # Este campo es constante por eso se pone directo al momento de la creación
                producto.estado = 'activo'

                if validar_creacion(producto_lote):
                    exito, msg, id = consultas.registrar(conn=conn, dato=producto_lote)
                    if exito:
                        ventana_actual.close()
                        ventana_actual = None
                        datos = consultas.cargar_tabla(conn)
                        ventana_secundaria['evt:{};det:list;act:list'.format(obtener_alias_controlador())].update(
                            values=datos)
                        ventana = ventana_secundaria
                    else:
                        msg = msg.replace('UNIQUE constraint failed:',
                                          'Se intenta registrar un valor duplicado (que no es permitido) para:')
                        psg.popup_error(msg, title='Error')

                else:
                    mensajes_error = listar_mensajes_errores_creacion()
                    indicadores_error = validar_condiciones_creacion(dato=producto_lote)
                    mensaje = '\n'.join(
                        [i[1] for i in filter(lambda x: not x[0], list(zip(indicadores_error, mensajes_error)))])
                    psg.popup_error(mensaje, title='Revise para continuar')
        elif cmd['det'] == 'update':
            if cmd['act'] == 'ok':
                producto = Producto_lote()
                producto_lote.producto_lote_id = valores['id']
                producto_lote.sku = valores['sku']
                producto_lote.nombre = valores['nombre']
                producto_lote.unidad = valores['unidad']
                producto_lote.costo_unitario = valores['costo-unitario']
                producto_lote.cantidad = valores['cantidad']
                producto_lote.disponible = valores['disponible']
                producto_lote.reservado = valores['reservado']
                producto_lote.dias_vida_util = valores['dias-vida-util']
                producto_lote.porcentaje_impuesto = valores['porcentaje-impuesto']
                producto_lote.monto_utilidad = valores['monto_utilidad']
                producto_lote.precio = valores['precio']
                producto_lote.redondeo = valores['redondeo']
                estado_activo = valores['estado-activo']
                estado_inactivo = valores['estado-inactivo']

                # Como estado lo recupera de un radiobutton hay que ver el estado de cada botón
                if estado_activo:
                    producto_lote.estado = 'activo'
                elif estado_inactivo:
                    producto_lote.estado = 'inactivo'
                else:
                    producto_lote.estado = ''

                if validar_actualizacion(producto_lote):
                    exito, msg, id = consultas.modificar(conn=conn, dato=producto_lote)
                    if exito:
                        ventana_actual.close()
                        ventana_actual = None
                        datos = consultas.cargar_tabla(conn)
                        ventana_secundaria['evt:{};det:list;act:list'.format(obtener_alias_controlador())].update(
                            values=datos)
                        ventana = ventana_secundaria
                    else:
                        msg = msg.replace('UNIQUE constraint failed:',
                                          'Se intenta registrar un valor duplicado (que no es permitido) para:')
                        psg.popup_error(msg, title='Error')
                else:
                    mensajes_error = listar_mensajes_errores_actualizacion()
                    indicadores_error = validar_condiciones_actualizacion(producto_lote)
                    mensaje = '\n'.join(
                        [i[1] for i in filter(lambda x: not x[0], list(zip(indicadores_error, mensajes_error)))])
                    psg.popup_error(mensaje, title='Revise para continuar')
        elif cmd['det'] == 'delete':
            if cmd['act'] == 'ok':
                id = valores['id']

                respuesta = psg.popup_yes_no('¿Desea continuar?',
                                             title='Confirmación')

                # Verificar la respuesta del usuario
                if respuesta == 'Yes':
                    consultas.eliminar(conn, int(id))

                ventana_actual.close()
                ventana_actual = None
                datos = consultas.cargar_tabla(conn)
                ventana_secundaria['evt:{};det:list;act:list'.format(obtener_alias_controlador())].update(values=datos)
                ventana = ventana_secundaria

    return ventana
