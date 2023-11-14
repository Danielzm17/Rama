from typing import Tuple, Optional, Any

import utils.validaciones as utils_validacion
import utils.ventana as utils_ventana

import PySimpleGUI as psg

from local.local import Local
import local.vista as vistas
import local.consultas as consultas


def obtener_alias_controlador() -> str:
    return 'local'


def listar_mensajes_errores_actualizacion() -> Tuple[str, ...]:
    # debe corresponder a lista de validación
    return ('Revise el nombre',
            'Revise el estado')


def validar_condiciones_actualizacion(dato: Local) -> Tuple[bool, ...]:
    if dato:
        # tiene que coincidir con el orden y cantidad de los mensajes en def listar_mensajes_errores_actualizacion()
        validacion = (
            not utils_validacion.validar_texto_vacio(dato.nombre),
            not utils_validacion.validar_texto_vacio(dato.estado)
        )
        return validacion
    else:
        return ()


def validar_actualizacion(dato: Local) -> bool:
    if dato:
        validacion = validar_condiciones_creacion(dato)
        return all(validacion)
    else:
        return False


def listar_mensajes_errores_creacion() -> Tuple[str, ...]:
    # debe corresponder a lista de validación
    return ('Revise el nombre', 'Revise el estado')


def validar_condiciones_creacion(dato: Local) -> Optional[Tuple[bool, ...]]:
    if dato:
        validacion = (
            not utils_validacion.validar_texto_vacio(dato.nombre),  # nombre
            not utils_validacion.validar_texto_vacio(dato.estado)  # estado
        )
        return validacion
    else:
        return None


def validar_creacion(dato: Local) -> bool:
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
        psg.popup_error('Intentando procesar un evento de lugar, pero se envió otro evento', 'Error de programación')
    else:
        if cmd['det'] == 'main':
            if cmd['act'] == 'create':
                ventana = vistas.crear_ventana_registro()
            elif cmd['act'] == 'update':
                nombre_tabla = 'evt:{};det:list;act:list'.format(obtener_alias_controlador())
                data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_secundaria,
                                                                               nombre_tabla=nombre_tabla,
                                                                               valores=valores)
                if data_selected:
                    selected = int(data_selected[0][0])
                    dato: Local = consultas.cargar(conn=conn, id=selected)
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
                    dato: Local = consultas.cargar(conn=conn, id=selected)
                    ventana = vistas.crear_ventana_eliminacion(dato)
                else:
                    psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')

        elif cmd['det'] == 'create':
            if cmd['act'] == 'ok':
                dato = Local()
                dato.nombre = valores['nombre']
                dato.estado = 'activo'
                dato.lugar_id = valores['lugar_id']

                if validar_creacion(dato):
                    exito, msg, id = consultas.registrar(conn=conn, dato=dato)
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
                    indicadores_error = validar_condiciones_creacion(dato=dato)
                    mensaje = '\n'.join(
                        [i[1] for i in filter(lambda x: not x[0], list(zip(indicadores_error, mensajes_error)))])
                    psg.popup_error(mensaje, title='Revise para continuar')


        elif cmd['det'] == 'update':
            if cmd['act'] == 'ok':
                dato = Local()
                dato.local_id = valores['id']
                dato.nombre = valores['nombre']
                dato.lugar_id = valores['lugar_id']
                estado_activo = valores['estado-activo']
                estado_inactivo = valores['estado-inactivo']

                # Como estado lo recupera de un radiobutton hay que ver el estado de cada botón
                if estado_activo:
                    dato.estado = 'activo'
                elif estado_inactivo:
                    dato.estado = 'inactivo'
                else:
                    dato.estado = ''

                if validar_actualizacion(dato):
                    exito, msg, id = consultas.modificar(conn=conn, dato=dato)
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
                    indicadores_error = validar_condiciones_actualizacion(dato)
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
