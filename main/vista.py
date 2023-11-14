import PySimpleGUI as psg
from config.iconos import *


def create_menu():
    """
    Crea el menú del usuario
    :return: Lista con las opciones del menú
    """
    # Cuando se activen los usuario, este menú debe ser dinámico
    return [
        [
            '&Archivo',
            [
                '&Salir'
            ]
        ],
        [
            '&Planificación de la producción',
            [
                '&Nueva planificación de la producción',
                '&Registro de capacidad diaria',
                '&Planificaciones registradas',
                '&Reportes de planificaciones registradas',
            ]
        ],

        [
            '&Operativos',
            [
                '&Clientes',
                '&Proveedores',
                'C&apacidad diaria'
            ]
        ],

        [
            '&Inventario',
            [
                '&Materias Primas',
                'M&aterias primas por proveedor',
                '&Lotes de materias primas',
                '&Productos',
                'L&otes de productos',
                '&Explosión de materiales (BOM)'
            ]
        ],

        [
            '&Ventas y pronósticos',
            [
                '&Importación de ventas',
                '&Resumen de ventas',
                '&Generar pronósticos',
            ]
        ],

        [
            '&Datos generales',
            [
                '&Lugar / Ubicaciones geográficas',
                '&Locales / Bodegas'
            ]
        ],

        [
            '&Reporte',
            [
                'Reporte de productos',
                'Reporte de materias primas',
                'Reporte de BOM',
                'Reporte de proyectos',
                'Reporte de clientes',
                'Reporte de proveedores',
                'Reporte de ventas',
                'Reporte de capacidad diaria',
                'Reporte de locales'
            ]
        ],
        [
            '&Importadores',
            [
                'Importar productos',
                'Importar materias primas',
                'Importar BOM',
                'Importar clientes',
                'Importar proveedores',
                'Importar ventas',
                'Importar capacidad diaria',
                'Importar locales'
            ]
        ],
        [
            'A&yuda',
            [
                '&Información de la aplicación, Terminos de uso y Licencia',
                '&Color'
            ]
        ]
    ]


def create_main_window():
    """
    Crea la pantalla principal solo con el menú
    :return: Pantalla (layout) principal
    """
    layout = [
        [
            psg.Menu(create_menu())
        ],
        [

        ]
    ]
    w = psg.Window('Aplicación de Ingeniería de Operaciones', layout, finalize=True, resizable=True, icon=icon_app_title)
    w.Maximize()
    return w


def create_project_window():
    layout = [[psg.Menu(create_menu())], []]
    w = psg.Window('Aplicación de Ingeniería de Operaciones', layout, finalize=True, resizable=True)
    w.Maximize()
    return w
