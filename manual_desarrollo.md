# Manual de desarrollo

Este trabajo fue pensando para ser desarrollado por el estudiantado de Ingeniería Industrial.
Que actualmente han llevado los cursos de:

Donde se utilizarán temas puntuales de los siguientes cursos:
- Principios de informática
  - Conocimientos básicos de Python (Programación estructurada)
- Tecnologías de Información
  - Normalización de bases de datos
  - Consultas de SQL
- Diseño de Sistemas de Información
  - Plantear Casos de Uso
  - Definición de requerimientos
- Ingeniería de Operaciones
  - BOM
  - MPS
  - MRP
  - Definición de casos de prueba con datos calculos correctamente

Para el desarrollo, y debido a ciertas limitaciones de conocimiento de arquitecturas de software, 
se propone un esquema programación estructura, separada por módulos, donde se agrupen
funciones / procedimientos según "funcionalidad".

Entre las funcionalidades a agrupar se tienen:
- Generación de pantallas (_view)
- Consultas (y comandos) a la base de datos (_consultas)
- Coordinación de ejecución de scripts (_controlador)

Principalmente, igual existirán otras categorías.  Debido a que su implementación
es por PySimpleGUI (PSG) y sus limitaciones de control de eventos y mensajes.
Se utilizará los eventos del PSG y en las ventanas campos invisibles, para registrar
información relevante.

En el caso de los campos invisibles se utilizarán principalmente dos, a través de sus "keys":
- --cmd-- que indicará el comando para que le entienda el ciclo principal.
- --id-- que será el 'ID' en la tabla del dato en uso.

## CRUD
Los CRUD se componen de dos tipos de ventanas:
- Las de tipo listado, donde aparecen los datos y tendrá acceso a los botones para:
  - Agregar
  - Modificar
  - Eliminar
- Las de tipo detalle, donde se puede manipular los datos de cada entidad
  - Botón aceptar
  - Botón Salir (este debe llamarse siempre así, proque controla la salida)