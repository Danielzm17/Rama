from config.botones import *
from config.iconos import *
import PySimpleGUI as psg
from materia_prima.consultas import *

def obtener_alias_controlador() -> str:
    return 'mat_pri'

def obtener_etiqueta_mensaje() -> str:
    return 'Materia prima'

def crear_ventana_inicio(conn=None):


    encabezado = ['Id', 'SKU', 'Nombre', 'Cantidad', 'Disponible', 'Reservado', 'Unidad',
                  'Costo Un.','Estado','Vida útil']

    data_values = list(cargar_tabla(conn))

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
            det='list',
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

    # Datos del combobox de unidades, si fuera de un tabla hay que tomarlo de una clase consultas
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Input(key='sku', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Input(key='nombre', size=(ancho_contenido, 1), expand_x=True)
        ],

        [
            psg.Text('Unidades', size=(ancho_etiqueta, 1)),
            psg.Combo(unidades, key='unidad', size=(10, 1), readonly=True, default_value=unidades[0],
                      expand_x=True)
        ],
        [
            psg.Text('Cantidad', size=(ancho_etiqueta, 1)),
            psg.Input(key='cantidad', expand_x=True)
        ],
        [
            psg.Text('Disponible', size=(ancho_etiqueta, 1)),
            psg.Input(key='disponible', expand_x=True)
        ],
        [
            psg.Text('Reservado', size=(ancho_etiqueta, 1)),
            psg.Input(key='reservado', expand_x=True),

        ],
        [
            psg.Text('Días de vida útil', size=(ancho_etiqueta, 1)),
            psg.Input(key='dias-vida-util', expand_x=True),
        ],
        [
            psg.Text('Costo unitario', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo-unitario', size=(ancho_contenido, 1), expand_x=True)
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


def crear_ventana_actualizacion(dato:MateriaPrima):
    ancho_etiqueta = 25
    ancho_contenido = 55
    # Datos del combobox de unidades, si fuera de un tabla hay que tomarlo de una clase consultas
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato.materia_prima_id, visible=True, key='id-txt', expand_x=True),
            psg.Input(visible=False, key='id', default_text=dato.materia_prima_id)
        ],
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Input(key='sku', size=(ancho_contenido, 1), expand_x=True, default_text=dato.sku)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Input(key='nombre', size=(ancho_contenido, 1), expand_x=True, default_text=dato.nombre)
        ],
        [
            psg.Text('Cantidad', size=(ancho_etiqueta, 1)),
            psg.Input(key='cantidad', expand_x=True, default_text=dato.cantidad)
        ],
        [
            psg.Text('Unidad', size=(ancho_etiqueta, 1)),
            psg.Combo(unidades, key='unidad', size=(10, 1), readonly=True, default_value=dato.unidad,
                      expand_x=True)
        ],
        [
            psg.Text('Costo unitario', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo-unitario', size=(ancho_contenido, 1), expand_x=True, default_text=dato.costo_unitario)
        ],
        [
            psg.Text('Disponible', key='disponible-lbl', size=(ancho_etiqueta, 1)),
            psg.Input(key='disponible', size=(ancho_contenido, 1), expand_x=True, default_text=dato.disponible)
        ],
        [
            psg.Text('Días de vida útil', key='dias-vida-util-lbl', size=(ancho_etiqueta, 1)),
            psg.Input(key='dias-vida-util', size=(ancho_contenido, 1), expand_x=True,
                      default_text=dato.dias_vida_util)
        ],
        [
            psg.Text('Reservado', key='reservado-lbl', size=(ancho_etiqueta, 1)),
            psg.Input(key='reservado', size=(ancho_contenido, 1), expand_x=True, default_text=dato.reservado)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default=dato.estado == 'activo', key='estado-activo', expand_x=True),
            psg.Radio('Inactivo', 'estado', default=dato.estado == 'inactivo', key='estado-inactivo', expand_x=True)
        ],
        [
            psg.Text('Fecha creación', key='creacion-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato.fecha_registro, key='creacion', expand_x=True)
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


def crear_ventana_eliminacion(dato:MateriaPrima):
    ancho_etiqueta = 25
    ancho_contenido = 55
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato.materia_prima_id, visible=True, key='id-txt', expand_x=True),
            psg.Input(key='id', visible=False, default_text=dato.materia_prima_id)
        ],
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Text(dato.sku, key='sku', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Text(dato.nombre, key='nombre', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Fecha creación', key='creacion-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato.fecha_registro, key='creacion', expand_x=True)
        ],
        [
            psg.Button('', tooltip='Eliminar', expand_x=True,
                       image_data=icon_general_aceptar,
                       button_color='DodgerBlue',
                       key='evt:{};det:{};act:{}'.format(obtener_alias_controlador(), 'delete', 'ok')),
            psg.Button('', tooltip='Salir', expand_x=True, key='Salir', image_data=icon_general_cancelar,
                       button_color='tomato')
        ]
    ]

    w = psg.Window('Eliminar : {}'.format(obtener_etiqueta_mensaje())
                   , layout
                   , finalize=True
                   , resizable=True
                   , size=(None, None)
                   , modal=True)
    return w
