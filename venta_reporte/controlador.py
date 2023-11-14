import utils.validaciones as utils_validacion
import utils.ventana as utils_ventana
import PySimpleGUI as psg


def obtener_alias_controlador() -> str:
    return 'venta_reporte'


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
        print('Controlador: [{}] sin implementar'.format(obtener_alias_controlador()))

    return ventana
