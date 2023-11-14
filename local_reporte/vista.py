from config.botones import *
from config.iconos import *
from materia_prima.consultas import *
import PySimpleGUI as psg
from pathlib import Path

def obtener_alias_controlador() -> str:
    return 'local_reporte'


def obtener_etiqueta_mensaje() -> str:
    return 'Reporte de local'


def generar_opciones_reporte_basico() -> psg.Tab:
    ancho_etiqueta = 20
    ancho_contenido = 55
    tamaño_etiqueta = (ancho_etiqueta, 1)
    tamaño_contenido = (ancho_contenido, 1)
    directorio_usuario = str(Path.home())
    return psg.Tab(
        title='General',
        expand_x=True,
        expand_y=True,
        key='tab-rep01',
        layout=[
            [
                psg.Frame(
                    title='Filtros',
                    expand_x=True,
                    expand_y=True,
                    layout=[
                        [
                            psg.Text('Destino'),
                            psg.Input(
                                default_text='',
                                key='destino-nombre'
                            ),
                            psg.FolderBrowse(
                                button_text='Buscar destino',
                                key='destino-folder',
                                enable_events=True,
                                initial_folder=directorio_usuario
                            )
                        ],
                        [
                            psg.Text('ID',
                                     size=tamaño_etiqueta),
                            psg.Input('',
                                      size=tamaño_contenido,
                                      key='rep01-filtro-id')
                        ],
                        [
                            psg.Text('Nombre',
                                     size=tamaño_etiqueta),
                            psg.Input('',
                                      size=tamaño_contenido,
                                      key='rep01-filtro-nombre')
                        ]
                    ]
                )
            ],
            [
                psg.Frame(
                    title='Ordernamiento',
                    expand_x=True,
                    expand_y=True,
                    layout=[
                        [psg.Text('Ordenar por:')],
                        [psg.Radio(text='ID',
                                   key='rep01-ordenar-id',
                                   group_id='rep01-ordenar',
                                   default=True)],
                        [psg.Radio(text='Nombre',
                                   key='rep01-ordenar-nombre',
                                   group_id='rep01-ordenar')],
                    ]
                )
            ]
        ]
    )



def crear_ventana_inicio(conn=None):
    # col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [

        [
            psg.TabGroup(
                [
                    [
                        generar_opciones_reporte_basico(),

                    ]
                ],
                key='Tab',
                expand_x=True
            )
        ],
        [
            crear_boton_barchart_med(evt=obtener_alias_controlador(),det='generar',act='generar'),
            crear_boton_salir_med()
        ],
        [
            psg.Input(visible=False, key='-cmd-', default_text='crud-{}'.format(obtener_alias_controlador()))
        ]
    ]

    w = psg.Window(
        'Listado : {}'.format(obtener_etiqueta_mensaje())
        , layout
        , finalize=True
        , resizable=True
        , modal=True
    )
    return w
