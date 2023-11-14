# MiniMRP-EII

## Introducción

Este es un proyecto demostrativo del proceso de cálculos de MRP2 (no incluye, CRP o PQR), solamente BOM, MPS y MRP.
Además, se incluye los catálogos (se entiende como catálogo como las ventana para realizar las operaciones básicas de
agregar, modificar y eliminar los datos (CRUD)) para cada una de las tablas de información (se detallarán más adelante).

Este proyecto forma parte de los esfuerzos del laboratorio del curso de Ingeniería de Operaciones (II-0703), 
de la Escuela de Ingeniería Industrial de la Universidad de Costa Rica, para aplicar los conocimientos adquiridos en
la teoría del curso.

## Tecnología usadas

En el desarrollo de esta solución se está utilizando las siguientes tecnologías:

- Python 3.10 o superior
- SQLite 3.0 o superior (incorporado en la distribución de Python)
- PySimpleGUI (se debe instalar a través de `pip install pysimplegui` )
- Openpyxl 3.1 o superior (se debe instalar a través de `pip install openpyxl` )

## Módulos planificados y componentes de la aplicación

Para esta versión se tiene planificadas las siguientes funcionalidades:
  1. Catálogos: Entre los CRUD descritos en esta versión se tienen:
     - Lugar
     - Local
     - Cliente
     - Proveedor
     - Ventas
     - Productos
       - Lotes de productos
     - Materias Primas
       - Lotes de materias primas


## Licencia

[Esta desarrollo se rige por la licencia CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

[^1]: Se implemento con unidades de ejemplo ('unidad', 'gramos', 'cc', 'cm').

<!--
## Add your files
```
cd existing_repo
git remote add origin https://gitlab.com/ii0703/minimrp-eii.git
git branch -M main
git push -uf origin main
```
-->