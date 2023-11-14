from typing import Tuple, Optional

import materia_prima.vista as vistas
import materia_prima.consultas as consultas
import utils.validaciones as utils_validacion
import utils.ventana as utils_ventana

import PySimpleGUI as psg

from materia_prima.materia_prima import MateriaPrima


def obtener_alias_controlador() -> str:
    return 'mat_pri'


def listar_mensajes_errores_actualizacion() -> Tuple[str, ...]:
    # debe corresponder a lista de validación
    return ('Revise SKU',
            'Revise el nombre',
            'Revise la cantidad',
            'Revise la unidad',
            'Revise el costo unitario',
            'Revise el estado')


def validar_condiciones_actualizacion(dato: MateriaPrima):
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


def validar_actualizacion(dato: MateriaPrima) -> bool:
    if dato:
        validacion = validar_condiciones_creacion(dato)
        return all(validacion)
    else:
        return False


def listar_mensajes_errores_creacion() -> Tuple[str, ...]:
    # debe corresponder a lista de validación
    return ('Revise SKU', 'Revise el nombre', 'Revise la cantidad', 'Revise la unidad', 'Revise el precio',
            'Revise el costo unitario', 'Revise el estado')


def validar_condiciones_creacion(dato: MateriaPrima) -> Optional[Tuple[bool, ...]]:
    if dato:
        validacion = (
            not utils_validacion.validar_texto_vacio(dato.sku),  # sku
            not utils_validacion.validar_texto_vacio(dato.nombre),  # nombre
            utils_validacion.validar_numero_real(dato.cantidad),  # cantidad
            not utils_validacion.validar_texto_vacio(dato.unidad),  # unidad
            utils_validacion.validar_numero_real(dato.disponible),  # disponible
            utils_validacion.validar_numero_real(dato.reservado),  # reservado
            utils_validacion.validar_numero_real(dato.costo_unitario),  # costo_unitario
            not utils_validacion.validar_texto_vacio(dato.estado),  # estado
            utils_validacion.validar_numero_real(dato.dias_vida_util)  # dias_vida_util
        )
        return validacion
    else:
        return None


def validar_creacion(dato: MateriaPrima) -> bool:
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
                    dato: MateriaPrima = consultas.cargar(conn=conn, id=selected)
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
                    dato: MateriaPrima = consultas.cargar(conn=conn, id=selected)
                    ventana = vistas.crear_ventana_eliminacion(dato)
                else:
                    psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')
        elif cmd['det'] == 'create':
            if cmd['act'] == 'ok':
                materia_prima = MateriaPrima()
                materia_prima.sku = valores['sku']
                materia_prima.nombre = valores['nombre']
                materia_prima.unidad = valores['unidad']
                materia_prima.costo_unitario = valores['costo-unitario']
                materia_prima.cantidad = valores['cantidad']
                materia_prima.disponible = valores['disponible']
                materia_prima.reservado = valores['reservado']
                materia_prima.dias_vida_util = valores['dias-vida-util']
                # Este campo es constante por eso se pone directo al momento de la creación
                materia_prima.estado = 'activo'

                if validar_creacion(materia_prima):
                    exito, msg, id = consultas.registrar(conn=conn, dato=materia_prima)
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
                    indicadores_error = validar_condiciones_creacion(dato=materia_prima)
                    mensaje = '\n'.join(
                        [i[1] for i in filter(lambda x: not x[0], list(zip(indicadores_error, mensajes_error)))])
                    psg.popup_error(mensaje, title='Revise para continuar')

        elif cmd['det'] == 'update':
            if cmd['act'] == 'ok':
                materia_prima = MateriaPrima()
                materia_prima.materia_prima_id = valores['id']
                materia_prima.sku = valores['sku']
                materia_prima.nombre = valores['nombre']
                materia_prima.unidad = valores['unidad']
                materia_prima.costo_unitario = valores['costo-unitario']
                materia_prima.cantidad = valores['cantidad']
                materia_prima.disponible = valores['disponible']
                materia_prima.reservado = valores['reservado']
                materia_prima.dias_vida_util = valores['dias-vida-util']
                estado_activo = valores['estado-activo']
                estado_inactivo = valores['estado-inactivo']

                # Como estado lo recupera de un radiobutton hay que ver el estado de cada botón
                if estado_activo:
                    materia_prima.estado = 'activo'
                elif estado_inactivo:
                    materia_prima.estado = 'inactivo'
                else:
                    materia_prima.estado = ''

                if validar_actualizacion(materia_prima):
                    exito, msg, id = consultas.modificar(conn=conn, dato=materia_prima)
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
                    indicadores_error = validar_condiciones_actualizacion(materia_prima)
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
