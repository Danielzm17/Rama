from json import detect_encoding
from typing import Optional, List, Tuple

from bom.consultas import *
from bom_componente.bom_componente import BomComponente
from bom_materia_prima.bom_materia_prima import BomMateriaPrima
from config.botones import *
from materia_prima.materia_prima import MateriaPrima
from producto.producto import Producto


def obtener_alias_controlador() -> str:
    return 'bom'


def obtener_etiqueta_mensaje() -> str:
    return 'Lista de materiales'


def crear_ventana_inicio(conn=None):
    encabezado = ['Id', 'SKU', 'Nombre', 'Versión', 'Tipo Receta',
                  'Estado', 'Ct. Cptes', 'Ct. Mat. Pr.', 'Ct. Optvo']

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
                      expand_x=True,
                      key='evt:{};det:list;act:list'.format(obtener_alias_controlador()))
        ],
        [
            psg.Text(
                'PARA AGREGAR UNA EXPLOSION DE MATERIALES, ' +
                'PRIMERO REGISTRE UN BOM. ' +
                'PARA AGREGAR MATERIALES O COMPONENTES, ' +
                'USE LA OPCION DE EDITAR',
                key='Texto', justification='center',
                expand_x=True,
                expand_y=True,
                background_color='yellow')
        ],
        crear_botones_crud_salir(evt=obtener_alias_controlador(),
                                 det='main-list',
                                 etiqueta=obtener_etiqueta_mensaje()
                                 ),
        [psg.Input(visible=False,
                   key='-cmd-',
                   default_text='crud-{}'.format(obtener_alias_controlador()))]
    ]

    w = psg.Window(
        'Listado : {}'.format(obtener_etiqueta_mensaje()),
        layout,
        finalize=True,
        resizable=True,
        modal=True
    )

    return w


def crear_ventana_registro():
    encabezado = ['Id', 'SKU', 'Nombre', 'Estado']

    col_anchos = [2, 4, 25, 5]
    layout = [
        [
            psg.Frame('PASO 01: Buscar el producto',
                      [
                          [
                              psg.Text('SKU: ', size=(15, 1)),
                              psg.Input('', key='sku', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(15, 1)),
                              psg.Input('', key='nombre', expand_x=True)
                          ],
                          [
                              crear_boton_buscar_peq(
                                  evt=obtener_alias_controlador(),
                                  det='add-bom',
                                  act='prod_find')
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso01')
        ],
        [
            psg.Frame('PASO 02: Seleccionar el producto',
                      [
                          [
                              psg.Table(values=[],
                                        headings=encabezado,
                                        max_col_width=30,
                                        num_rows=5,
                                        col_widths=col_anchos,
                                        justification='center',
                                        auto_size_columns=False,
                                        enable_events=True,
                                        select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                        expand_x=True,
                                        expand_y=True,
                                        key='evt:{};det:add-bom;act:prod_list'.format(obtener_alias_controlador()))
                          ],
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso02',
                      visible=True)
        ],
        [
            psg.Frame('PASO 03: Detallar información de la explosión de materiales',
                      [

                          [
                              psg.Input('', key='producto_id', visible=False),
                              psg.Text('SKU: ', size=(20, 1)),
                              psg.Text('', key='producto_sku', expand_x=True)
                          ],
                          [
                              psg.Text('Producto: ', size=(20, 1)),
                              psg.Text('', key='producto_nombre', expand_x=True)
                          ],
                          [
                              psg.Text('Version: ', size=(20, 1)),
                              psg.Input('', key='version', expand_x=True)
                          ],
                          [
                              psg.Text('Tipo de receta: ', size=(20, 1)),
                              psg.Radio('Principal', 'receta', key='receta-principal', expand_x=True, default=True),
                              psg.Radio('Alterna', 'receta', key='receta-alterna', expand_x=True)
                          ],
                          [
                              psg.Text('Comentario: ', size=(20, 1)),
                              psg.Multiline(autoscroll=True, expand_x=True, expand_y=True, key='comentario',
                                            size=(3, 3))
                          ],
                          [
                              psg.Text('Costo operativos: ', size=(20, 1)),
                              psg.Input('', key='costo-operativo', expand_x=True)
                          ],
                          [
                              psg.Text('Tiempo de fabricación: ', size=(20, 1)),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-horas'),
                              psg.Text('h', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-minutos'),
                              psg.Text('m', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-segundos'),
                              psg.Text('s', justification='left')
                          ],
                          [
                              psg.Text('Estado: ', size=(20, 1)),
                              psg.Radio('Activo', 'estado', key='estado-activo', expand_x=True, default=True),
                              psg.Radio('Inactivo', 'estado', key='estado-inactivo', expand_x=True)
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso03',
                      visible=True)
        ],
        crear_botones_aceptar_cancelar(obtener_alias_controlador(),
                                       'Registrar {}'.format(obtener_alias_controlador()),
                                       'add-bom',
                                       'create',
                                       disabled=True)
    ]

    w = psg.Window('Registrar : {}'.format(obtener_etiqueta_mensaje()),
                   layout,
                   finalize=True,
                   resizable=True,
                   modal=True)
    return w


def crear_ventana_edicion_bom(bom: Bom,
                              producto: Producto,
                              componentes: List[Tuple[BomComponente, Producto]],
                              materias_primas:List[Tuple[BomMateriaPrima, MateriaPrima]]):
    ancho_etiqueta = 25
    ancho_contenido = 55

    treedata = psg.TreeData()
    treedata.insert('', 'raiz', producto.nombre, [0, 0, 0])
    treedata.insert('raiz', 'comp', 'Componentes', [0, 0, 0])
    for componente, p in componentes:
        treedata.insert('comp', 'comp:{}'.format(componente.bom_componentes_id), p.nombre,
                        [componente.cantidad, componente.costo_unitario, componente.cantidad * componente.costo_unitario])

    treedata.insert('raiz', 'mp', 'Materias primas', [0, 0, 0])
    for componente, mp in materias_primas:
        treedata.insert('mp', 'matpri:{}'.format(componente.bom_materia_prima_id), mp.nombre,
                        [componente.cantidad, componente.costo_unitario, componente.cantidad * componente.costo_unitario])

    frame_arbol = psg.Frame('Árbol de explosión de materiales',
                            [
                                [
                                    psg.Input(visible=False, key='bom-id', default_text=bom.bom_id)
                                ],
                                [
                                    psg.Tree(data=treedata,
                                             headings=['Ctd. Un.', 'Costo Un.', 'Costo Total'],
                                             auto_size_columns=True,
                                             num_rows=10,
                                             col0_width=25,
                                             key='-TREE-',
                                             show_expanded=True,
                                             enable_events=False,
                                             select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                             expand_x=True,
                                             expand_y=True,
                                             )
                                ],
                            ],
                            expand_x=True,
                            expand_y=True)

    frame_control_materia_prima = psg.Frame('Edición Materias primas',
                                            [
                                                [
                                                    crear_boton_agregar_med(evt=obtener_alias_controlador(),
                                                                            det='detail-materia-prima',
                                                                            act='add')
                                                ],
                                                [
                                                    crear_boton_modificar_med(evt=obtener_alias_controlador(),
                                                                              det='detail-materia-prima',
                                                                              act='update')
                                                ],
                                                [
                                                    crear_boton_eliminar_med(evt=obtener_alias_controlador(),
                                                                             det='detail-materia-prima',
                                                                             act='delete')
                                                ],
                                            ],
                                            expand_x=True,
                                            expand_y=True)

    frame_control_componente = psg.Frame('Edición Componentes',
                                         [
                                             [
                                                 crear_boton_agregar_med(evt=obtener_alias_controlador(),
                                                                         det='detail-componente',
                                                                         act='add')
                                             ],
                                             [
                                                 crear_boton_modificar_med(evt=obtener_alias_controlador(),
                                                                           det='detail-componente',
                                                                           act='update')
                                             ],
                                             [
                                                 crear_boton_eliminar_med(evt=obtener_alias_controlador(),
                                                                          det='detail-componente',
                                                                          act='delete')
                                             ],
                                         ],
                                         expand_x=True,
                                         expand_y=True)

    frame_bom_info = psg.Frame('Información general',
                               [
                                   [
                                       psg.Input(default_text=producto.producto_id, key='producto-id', expand_x=True,
                                                 visible=False)
                                   ],
                                   [
                                       psg.Text('SKU', size=(ancho_etiqueta, 1), background_color='white',
                                                text_color='black'),
                                       psg.Text(producto.sku, key='sku-producto', size=(ancho_contenido, 1),
                                                expand_x=True, background_color='white', text_color='black'),
                                       crear_boton_informacion_peq(evt=obtener_alias_controlador())
                                   ],
                                   [
                                       psg.Text('Nombre', size=(ancho_etiqueta, 1), background_color='white',
                                                text_color='black'),
                                       psg.Text(producto.nombre, key='nombre-producto', size=(ancho_contenido, 1),
                                                expand_x=True, background_color='white', text_color='black'),
                                   ]
                               ],
                               expand_x=True,
                               expand_y=True)

    layout_col_izquierda = \
        [
            [
                frame_arbol
            ],
            [
                frame_bom_info
            ]
        ]

    layout_col_derecha = \
        [
            [
                frame_control_materia_prima
            ],
            [
                frame_control_componente
            ],
            [
                crear_boton_salir_med()
            ]
        ]

    layout = [
        [
            psg.Column(layout_col_izquierda,
                       expand_x=True,
                       expand_y=True),
            psg.Column(layout_col_derecha,
                       expand_x=True,
                       expand_y=True)
        ],

    ]

    w = psg.Window('Modificar : {}'.format(obtener_etiqueta_mensaje()),
                   layout,
                   finalize=True,
                   resizable=True,
                   modal=True)
    return w


def crear_ventana_bom_edicion(dato=None):
    ancho_etiqueta = 25
    ancho_contenido = 55

    layout = [
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Text(dato[2], key='sku-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Text(dato[3], key='nombre-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Versión', size=(ancho_etiqueta, 1)),
            psg.Input(key='version-producto', size=(ancho_contenido, 1), expand_x=True,
                      default_text=dato[4])
        ],
        [
            psg.Text('Comentario', size=(ancho_etiqueta, 1)),
            psg.Multiline(key='comentario-producto', size=(ancho_contenido, 3), expand_x=True,
                          default_text=dato[6], )
        ],
        [
            psg.Text('Costo operativos', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo-operativos-producto', size=(ancho_contenido, 1),
                      expand_x=True,
                      default_text=dato[9])
        ],
        [
            psg.Text('Tipo Receta', key='receta-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Primaria', 'receta', default='Receta principal' == dato[5],
                      key='receta-primaria-producto',
                      expand_x=True),
            psg.Radio('Alternativa', 'receta', default='Receta alterna' == dato[5],
                      key='receta-alternativa-producto',
                      expand_x=True)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default='Activo' == dato[12],
                      key='estado-activo-producto',
                      expand_x=True),
            psg.Radio('Inactivo', 'estado', default='Inactivo' == dato[12],
                      key='estado-inactivo-producto',
                      expand_x=True)
        ],
        [
            crear_boton_modificar(evt=obtener_alias_controlador()),
            crear_boton_eliminar(evt=obtener_alias_controlador())
        ]
    ]

    w = psg.Window(
        'Edición : {}'.format(obtener_etiqueta_mensaje()),
        layout,
        finalize=True,
        resizable=True,
        modal=True
    )

    return w


def crear_ventana_bom_eliminar(bom: Bom, producto: Producto):
    ancho_etiqueta = 25
    ancho_contenido = 55

    layout = [
        [
            psg.Input(default_text=bom.bom_id, key='bom-id', visible=False, readonly=True),
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Text(producto.sku, key='sku-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Text(producto.nombre, key='nombre-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Versión', size=(ancho_etiqueta, 1)),
            psg.Text(bom.version, expand_x=True)
        ],
        [
            psg.Text('Comentario', size=(ancho_etiqueta, 1)),
            psg.Text(bom.comentario, expand_x=True)
        ],
        [
            psg.Text('Costo operativos', size=(ancho_etiqueta, 1)),
            psg.Text(bom.costo_operativos, expand_x=True)
        ],
        [
            psg.Text('Tipo Receta', key='receta-lbl', size=(ancho_etiqueta, 1)),
            psg.Text('Principal' if bom.receta_principal else 'Alternativa', expand_x=True)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Text('Activo' if bom.estado else 'Inactivo', expand_x=True)
        ],
        [
            psg.Button('', tooltip='Eliminar', expand_x=True,
                       image_data=icon_general_aceptar,
                       button_color='DodgerBlue',
                       key='evt:{};det:{};act:{}'.format(obtener_alias_controlador(), 'main-list', 'do-delete')),
            psg.Button('', tooltip='Salir', expand_x=True, key='Salir', image_data=icon_general_cancelar,
                       button_color='tomato')
        ]
    ]

    w = psg.Window(
        'Edición : {}'.format(obtener_alias_controlador()),
        layout,
        finalize=True,
        resizable=True,
        modal=True
    )

    return w


def crear_ventana_registro_materia_prima_en_bom(bom: Bom):
    encabezado = ['Id', 'SKU', 'Nombre', 'Unidad']
    ancho_etiqueta = 25
    ancho_contenido = 55
    # Datos del combobox de unidades, si fuera de un tabla hay que tomarlo de una clase consultas
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    data_values = []


    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [
        [
            psg.Frame('Seleccionar Materia Prima',
                      [
                          [
                              psg.Text('SKU: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='sku-buscar', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='nombre-buscar', expand_x=True)
                          ],
                          [
                              crear_boton_buscar_peq(obtener_alias_controlador(),
                                                     det='detail-materia-prima',
                                                     act='buscar')
                          ],
                          [
                              psg.Table(values=data_values,
                                        headings=encabezado,
                                        max_col_width=30,
                                        num_rows=10,
                                        col_widths=col_widths,
                                        justification='center',
                                        auto_size_columns=True,
                                        enable_events=True,
                                        select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                        expand_x=True,
                                        expand_y=True,
                                        key='evt:{};det:detail-materia-prima;act:select-materia-prima'.format(obtener_alias_controlador())
                                        )
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso02',
                      visible=True)
        ],
        [
            psg.Frame('Detallar información del Materia Prima',
                      [

                          [
                              psg.Input(bom.bom_id, key='bom-id', visible=False),
                              psg.Input('', key='materia-prima-id', visible=False),
                              psg.Text('SKU: ', size=(ancho_etiqueta, 1)),
                              psg.Text('', key='sku', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(ancho_etiqueta, 1)),
                              psg.Text('', key='nombre', expand_x=True)
                          ],
                          [
                              psg.Text('Cantidad: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='cantidad', expand_x=True)
                          ],
                          [
                              psg.Text('Unidad', size=(ancho_etiqueta, 1)),
                              psg.Combo(unidades, key='unidad', size=(10, 1), readonly=True,
                                        expand_x=True)
                          ],
                          [
                              psg.Text('Costo operativos: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='costo-operativo', expand_x=True)
                          ],
                          [
                              psg.Text('Tiempo de fabricación: ', size=(ancho_etiqueta, 1)),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-horas'),
                              psg.Text('h', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-minutos'),
                              psg.Text('m', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-segundos'),
                              psg.Text('s', justification='left')
                          ],
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso03',
                      visible=True)
        ],
        crear_botones_aceptar_cancelar(obtener_alias_controlador(),
                                       'Registrar materia prima',
                                       'detail-materia-prima',
                                       'do-add')
    ]

    w = psg.Window('Registrar una materia prima en la explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   modal=True)
    return w


def crear_ventana_registro_componente_en_bom(bom: Bom):
    encabezado = ['Id', 'SKU', 'Nombre', 'Unidad']
    ancho_etiqueta = 25
    ancho_contenido = 55
    # Datos del combobox de unidades, si fuera de un tabla hay que tomarlo de una clase consultas
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    data_values = []


    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [
        [
            psg.Frame('Seleccionar componente',
                      [
                          [
                              psg.Text('SKU: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='sku-buscar', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='nombre-buscar', expand_x=True)
                          ],
                          [
                              crear_boton_buscar_peq(obtener_alias_controlador(),
                                                     det='detail-componente',
                                                     act='buscar')
                          ],
                          [
                              psg.Table(values=data_values,
                                        headings=encabezado,
                                        max_col_width=30,
                                        num_rows=10,
                                        col_widths=col_widths,
                                        justification='center',
                                        auto_size_columns=True,
                                        enable_events=True,
                                        select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                        expand_x=True,
                                        expand_y=True,
                                        key='evt:{};det:detail-componente;act:select-componente'.format(obtener_alias_controlador())
                                        )
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso02',
                      visible=True)
        ],
        [
            psg.Frame('Detallar información del componente',
                      [

                          [
                              psg.Input(bom.bom_id, key='bom-id', visible=False),
                              psg.Input('', key='producto-id', visible=False),
                              psg.Text('SKU: ', size=(ancho_etiqueta, 1)),
                              psg.Text('', key='sku', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(ancho_etiqueta, 1)),
                              psg.Text('', key='nombre', expand_x=True)
                          ],
                          [
                              psg.Text('Cantidad: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='cantidad', expand_x=True)
                          ],
                          [
                              psg.Text('Unidad', size=(ancho_etiqueta, 1)),
                              psg.Combo(unidades, key='unidad', size=(10, 1), readonly=True,
                                        expand_x=True)
                          ],
                          [
                              psg.Text('Costo operativos: ', size=(ancho_etiqueta, 1)),
                              psg.Input('', key='costo-operativo', expand_x=True)
                          ],
                          [
                              psg.Text('Tiempo de fabricación: ', size=(ancho_etiqueta, 1)),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-horas'),
                              psg.Text('h', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-minutos'),
                              psg.Text('m', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-segundos'),
                              psg.Text('s', justification='left')
                          ],
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso03',
                      visible=True)
        ],
        crear_botones_aceptar_cancelar(obtener_alias_controlador(),
                                       'Registrar producto',
                                       'detail-componente',
                                       'do-add')
    ]

    w = psg.Window('Registrar un componente en la explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   modal=True)
    return w