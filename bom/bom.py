class Bom:
    def __init__(self):
        self.bom_id = 0
        self.producto_id = 0
        self.version = ''
        self.receta_principal = False
        self.comentario = ''
        self.costo_acumulado_componentes = 0
        self.costo_acumulado_materia_prima = 0
        self.costo_operativos = 0
        self.costo_total = 0
        self.tiempo_fabricacion = 0
        self.fecha_registro = ''
        self.estado = ''