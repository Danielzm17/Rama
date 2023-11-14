def centrar_ventana(ventana):
    ventana.finalize()
    screen_width, screen_height = ventana.get_screen_dimensions()
    win_width, win_height = ventana.size
    x, y = (screen_width - win_width) // 2, (screen_height - win_height) // 2
    ventana.move(x, y)

def obtener_datos_seleccionado_tabla(ventana, nombre_tabla, valores):
    tabla = ventana[nombre_tabla]
    valores_tabla = tabla.Values
    datos_seleccionados = [valores_tabla[row] for row in valores[nombre_tabla]]
    return datos_seleccionados