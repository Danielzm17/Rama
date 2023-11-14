from config.botones import *
from config.iconos import *
from producto_lote.consultas import *
import PySimpleGUI as psg

def obtener_alias_controlador() -> str:
    return 'producto_lote'

def obtener_etiqueta_mensaje() -> str:
    return 'Producto_lote'

def crear_ventana_inicio(conn=None):


    encabezado = ['Id', 'SKU', 'Nombre', 'Costo', 'Precio', 'Cantidad','Vida útil']

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
            etiqueta=obtener_etiqueta_mensaje()
        ),
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
            psg.Text('Costo', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Precio', size=(ancho_etiqueta, 1)),
            psg.Input(key='precio', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Cantidad', size=(ancho_etiqueta, 1)),
            psg.Input(key='cantidad', expand_x=True)
        ],
        [
            psg.Text('Días de vida útil', size=(ancho_etiqueta, 1)),
            psg.Input(key='dias-vida-util', expand_x=True),
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


def crear_ventana_actualizacion(dato:Producto_lote):
    ancho_etiqueta = 25
    ancho_contenido = 55
    # Datos del combobox de unidades, si fuera de un tabla hay que tomarlo de una clase consultas
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato.producto_lote_id, visible=True, key='id-txt', expand_x=True),
            psg.Input(visible=False, key='id', default_text=dato.producto_lote_id)
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
            psg.Text('Costo', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo', size=(ancho_contenido, 1), expand_x=True, default_text=dato.costo_unitario)
        ],
        [
            psg.Text('Precio', size=(ancho_etiqueta, 1)),
            psg.Input(key='precio', size=(ancho_contenido, 1), expand_x=True, default_text=dato.precio)
        ],
        [
            psg.Text('Cantidad', size=(ancho_etiqueta, 1)),
            psg.Input(key='cantidad', expand_x=True, default_text=dato.cantidad)
        ],
        [
            psg.Text('Días de vida útil', size=(ancho_etiqueta, 1)),
            psg.Input(key='dias-vida-util', expand_x=True, default_text=dato.dias_vida_util)
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


def crear_ventana_eliminacion(dato:Producto_lote):
    ancho_etiqueta = 25
    ancho_contenido = 55
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato.producto_lote_id, visible=True, key='id-txt', expand_x=True),
            psg.Input(key='id', visible=False, default_text=dato.producto_lote_id)
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
