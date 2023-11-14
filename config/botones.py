import PySimpleGUI as psg
from config.iconos import *


def crear_boton_aceptar(evt, tooltip='Aceptar', det='create', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_check_32, button_color=color_aceptar, disabled=disabled)


def crear_boton_aceptar_med(evt, tooltip='Aceptar', det='create', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_check_24, button_color=color_aceptar, disabled=disabled)


def crear_boton_aceptar_peq(evt, tooltip='Aceptar', det='acept', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_check_16, button_color=color_aceptar, disabled=disabled)


def crear_boton_agregar(evt, tooltip='Agregar', det='add', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_add_32, button_color=color_agregar, disabled=disabled)


def crear_boton_agregar_med(evt, tooltip='Agregar', det='add', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_add_24, button_color=color_agregar, disabled=disabled)


def crear_boton_agregar_peq(evt, tooltip='Agregar', det='add', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_add_16, button_color=color_agregar, disabled=disabled)


def crear_boton_buscar(evt, tooltip='Buscar', det='find', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_loupe32, button_color=color_aceptar, disabled=disabled)


def crear_boton_buscar_med(evt, tooltip='Buscar', det='find', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_loupe24, button_color=color_aceptar, disabled=disabled)


def crear_boton_buscar_peq(evt, tooltip='Buscar', det='find', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_loupe16, button_color=color_aceptar, disabled=disabled)


def crear_boton_informacion(evt, tooltip='Información', det='info', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_info_32, button_color=color_informacion, disabled=disabled)


def crear_boton_informacion_med(evt, tooltip='Información', det='info', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_info_24, button_color=color_informacion, disabled=disabled)


def crear_boton_informacion_peq(evt, tooltip='Información', det='info', act='ok', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_info_16, button_color=color_informacion, disabled=disabled)


def crear_boton_cancelar(disabled=False):
    return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_delete_32,
                      button_color=color_cancelar, disabled=disabled)


def crear_boton_cancelar_med(disabled=False):
    return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_delete_24,
                      button_color=color_cancelar, disabled=disabled)


def crear_boton_cancelar_peq(disabled=False):
    return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_delete_16,
                      button_color=color_cancelar, disabled=disabled)


def crear_botones_aceptar_cancelar(evt, tooltip, det, act, disabled=False):
    return [crear_boton_aceptar(evt, tooltip=tooltip, det=det, act=act, disabled=disabled), crear_boton_cancelar()]


def crear_boton_registrar(evt, tooltip='Registrar', det='list', act='create', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_add_32, button_color=color_agregar, disabled=disabled)


def crear_boton_registrar_med(evt, tooltip='Registrar', det='list', act='create', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_add_24, button_color=color_agregar, disabled=disabled)


def crear_boton_registrar_peq(evt, tooltip='Registrar', det='list', act='create', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_add_16, button_color=color_agregar, disabled=disabled)


def crear_boton_modificar(evt, tooltip='Modificar', det='list', act='update', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_hashtag_32, button_color=color_modificar, disabled=disabled)


def crear_boton_modificar_med(evt, tooltip='Modificar', det='list', act='update', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_hashtag_24, button_color=color_modificar, disabled=disabled)


def crear_boton_modificar_peq(evt, tooltip='Modificar', det='list', act='update', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      image_data=icon_hashtag_16, button_color=color_modificar, disabled=disabled)


def crear_boton_eliminar(evt, tooltip='Eliminar', det='list', act='delete', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_eliminar, image_data=icon_substraction_32, disabled=disabled)


def crear_boton_eliminar_med(evt, tooltip='Eliminar', det='list', act='delete', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_eliminar, image_data=icon_substraction_24, disabled=disabled)


def crear_boton_eliminar_peq(evt, tooltip='Eliminar', det='list', act='delete', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_eliminar, image_data=icon_substraction_16, disabled=disabled)

def crear_boton_barchart(evt, tooltip='Generar reporte', det='reportar', act='reporte', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_barchart32, disabled=disabled)


def crear_boton_barchart_med(evt, tooltip='Generar reporte', det='reportar', act='reporte', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_barchart24, disabled=disabled)


def crear_boton_barchart_peq(evt, tooltip='Generar reporte', det='reportar', act='reporte', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_barchart16, disabled=disabled)

def crear_botones_crud(evt, det, etiqueta, disabled=False):
    return [crear_boton_registrar(evt=evt,
                                  det=det,
                                  tooltip=f'Registrar {etiqueta}',
                                  disabled=disabled),
            crear_boton_modificar(evt=evt,
                                  det=det,
                                  tooltip=f'Modificar {etiqueta}',
                                  disabled=disabled),
            crear_boton_eliminar(evt=evt,
                                 det=det,
                                 tooltip=f'Eliminar {etiqueta}',
                                 disabled=disabled)]


# def crear_boton_salir(disabled=False):
#     return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_return32,
#                       button_color='tomato3', disabled=disabled)


def crear_boton_salir(disabled=False):
    return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_return32,
                      button_color=color_salir, disabled=disabled)


def crear_boton_salir_med(disabled=False):
    return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_return24,
                      button_color=color_salir, disabled=disabled)


def crear_boton_salir_peq(disabled=False):
    return psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_return16,
                      button_color=color_salir, disabled=disabled)

def crear_boton_download(evt, tooltip='Descargar', det='descargar', act='descarga', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_download32, disabled=disabled)


def crear_boton_download_med(evt, tooltip='Descargar', det='descargar', act='descarga', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_download24, disabled=disabled)


def crear_boton_download_peq(evt, tooltip='Subir', det='subir', act='subida', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_upload16, disabled=disabled)

def crear_boton_upload(evt, tooltip='Subir', det='subir', act='subida', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_upload32, disabled=disabled)


def crear_boton_upload_med(evt, tooltip='Subir', det='subir', act='subida', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_upload24, disabled=disabled)


def crear_boton_upload_peq(evt, tooltip='Descargar', det='descargar', act='descarga', disabled=False):
    return psg.Button('', tooltip=tooltip, key=f'evt:{evt};det:{det};act:{act}', expand_x=True,
                      button_color=color_buscar, image_data=icon_download32, disabled=disabled)

def crear_botones_crud_salir(evt, det, etiqueta, disabled=False):
    botones = crear_botones_crud(evt=evt,
                                 det=det,
                                 etiqueta=etiqueta,
                                 disabled=disabled)
    botones.append(crear_boton_salir())
    return botones
