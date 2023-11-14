from config.botones import *
from config.iconos import *
import PySimpleGUI as psg

import local.consultas as consultas_local
from local.local import Local


def obtener_alias_controlador() -> str:
    return 'local'

def obtener_etiqueta_mensaje() -> str:
    return 'Local'

def crear_ventana_inicio(conn=None):


    encabezado = ['Id', 'Nombre', 'Estado', 'ID de lugar']

    data_values = list(consultas_local.cargar_tabla(conn))

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [

        [
            psg.Table(values=data_values,
                      headings=encabezado,
                      max_col_width=30,
                      num_rows=25,
                      col_widths=col_widths,
                      justification='center',
                      auto_size_columns=False,
                      enable_events=True,
                      select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                      key='evt:{};det:{};act:{}'.format(obtener_alias_controlador(),'list','list'))
        ],
        crear_botones_crud_salir(
            evt=obtener_alias_controlador(),
            det='main',
            etiqueta=obtener_etiqueta_mensaje()),
        [psg.Input(visible=False, key='-cmd-', default_text='crud-{}'.format(obtener_alias_controlador()))]
    ]

    w = psg.Window(
        'Listado : {}'.format(obtener_etiqueta_mensaje())
        , layout
        , finalize=True
        , resizable=True
        , size=(None, None)
        , modal=True
    )
    return w

def crear_ventana_registro():
    ancho_etiqueta = 20
    ancho_contenido = 55


    layout = [

        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Input(key='nombre', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('ID de lugar', size=(ancho_etiqueta, 1)),
            psg.Input(key='lugar_id', size=(ancho_contenido, 1),  expand_x=True)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default=True, key='estado-activo', expand_x=True),
        ],
        crear_botones_aceptar_cancelar(obtener_alias_controlador(),'Registrar {}'.format(obtener_etiqueta_mensaje()),'create','ok')
    ]

    w = psg.Window('Registrar : {}'.format(obtener_etiqueta_mensaje())
                   , layout
                   , finalize=True
                   , resizable=True
                   , size=(None, None)
                   , modal=True)
    return w

def crear_ventana_actualizacion(dato:Local):
    ancho_etiqueta = 25
    ancho_contenido = 55
    # Datos del combobox de unidades, si fuera de un tabla hay que tomarlo de una clase consultas
    #unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato.local_id, visible=True, key='id-txt', expand_x=True),
            psg.Input(visible=False, key='id', default_text=dato.local_id)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Input(key='nombre', size=(ancho_contenido, 1), expand_x=True, default_text=dato.nombre)
        ],
        [
            psg.Text('ID de lugar', size=(ancho_etiqueta, 1)),
            psg.Input(key='lugar_ id', size=(ancho_contenido, 1), expand_x=True, default_text=dato.lugar_id)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default=dato.estado == 'activo', key='estado-activo', expand_x=True),
            psg.Radio('Inactivo', 'estado', default=dato.estado == 'inactivo', key='estado-inactivo', expand_x=True)
        ],
        crear_botones_aceptar_cancelar(obtener_alias_controlador(), 'Modificar {}'.format(obtener_etiqueta_mensaje()), 'update', 'ok')
    ]

    w = psg.Window('Modificar : {}'.format(obtener_etiqueta_mensaje())
                   , layout
                   , finalize=True
                   , resizable=True
                   , size=(None, None)
                   , modal=True)
    return w