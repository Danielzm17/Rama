from config.botones import *
from config.iconos import *
import PySimpleGUI as psg
from pathlib import Path


def obtener_alias_controlador() -> str:
    return 'producto_importar'


def obtener_etiqueta_mensaje() -> str:
    return 'Productos'


def crear_ventana_inicio(conn=None):
    directorio_usuario = str(Path.home())

    layout = [

        [
            psg.Column(
                expand_x=True,
                expand_y=True,
                layout=[
                    [psg.Text('Generar plantilla')],
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
                        crear_boton_download_med(evt=obtener_alias_controlador(),
                                                 det='plantilla',
                                                 act='procesar')
                    ]
                ]
            ),
            psg.Column(
                expand_x=True,
                expand_y=True,
                layout=[
                    [psg.Text('Importar datos')],
                    [
                        psg.Text('Origen'),
                        psg.Input(
                            default_text='',
                            key='origen-nombre'
                        ),
                        psg.FileBrowse(
                            button_text='Importar datos',
                            key='origen-archivo',
                            file_types=(('Archivos de excel', '*.xlsx'),),
                            enable_events=True,
                            initial_folder=directorio_usuario)
                    ],
                    [
                        crear_boton_upload_med(evt=obtener_alias_controlador(),
                                               det='importar',
                                               act='procesar')
                    ]
                ]
            )
        ],
        [
            crear_boton_salir_med()
        ],
        [
            psg.Text(text='', key='mensaje-error', text_color='red', expand_x=True, justification='center')
        ],
        [
            psg.Input(visible=False, key='-cmd-', default_text='crud-{}'.format(obtener_alias_controlador()))
        ]
    ]

    w = psg.Window(
        'Importar y exportar : {}'.format(obtener_etiqueta_mensaje())
        , layout
        , finalize=True
        , resizable=True
        , modal=True
    )
    return w
