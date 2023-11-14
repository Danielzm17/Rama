import sqlite3

def crear_conexion(nombre = 'ii0703.db'):
    conn = sqlite3.connect(nombre)
    return conn


def verificar_base_nueva(conn = None):
    sql = '''
            select
                count(*) as total 
            from 
                sqlite_master 
            where 
                type='table';
          '''
    resultado = conn.execute(sql).fetchone()
    return resultado[0] == 0


def crear_tablas(conn = None):
    sql = '''
/*
ESTA TABLA ES PARA ESTABLECER LOS LUGARES GEOGRAFICOS
*/
CREATE TABLE lugar (
    lugar_id                            INTEGER     NOT NULL 
                                        CONSTRAINT  lugar_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    nombre                              TEXT        NOT NULL,
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    CONSTRAINT lugar_uq_nombre UNIQUE (nombre),
    CONSTRAINT lugar_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado'))
);
PRAGMA ignore_check_constraints = 1;
insert into lugar (lugar_id, nombre) values (1000,'Desconocido');
PRAGMA ignore_check_constraints = 0;


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER lugar_on_delete
    BEFORE DELETE ON lugar
    BEGIN
        UPDATE lugar SET estado = 'eliminado' WHERE lugar_id = old.lugar_id;
        SELECT (RAISE(IGNORE));
    END;


/*
ESTA TABLA ES PARA ESTABLECER LOS LOCALES DE LA EMPRESA, PUEDE SER TIENDAS O BODEGAS
*/
CREATE TABLE local (
    local_id                            INTEGER     NOT NULL 
                                        CONSTRAINT  local_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    nombre                              TEXT        NOT NULL,
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    lugar_id                            INTEGER     NOT NULL,
    CONSTRAINT local_uq_nombre UNIQUE (nombre),
    CONSTRAINT local_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT local_fk_lugar_id FOREIGN KEY (lugar_id) 
        REFERENCES lugar
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(local);
PRAGMA ignore_check_constraints = 1;
insert into local (local_id, nombre, lugar_id) values (1000,'Local principal', 1000);
PRAGMA ignore_check_constraints = 0;


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER local_on_delete
    BEFORE DELETE ON local
    BEGIN
        UPDATE local SET estado = 'eliminado' WHERE local_id = old.local_id;
        SELECT (RAISE(IGNORE));
    END;



/*
EN ESTA TABLA SE REGISTRA LA INFORMACION DEL CLIENTE,
TIENE UN CLIENTE POR GENERICO EN CASO DE DESCONOCER EL CLIENTE O
NO NOS INTERESA REGISTRAR UN CLIENTE ESPECIFICO
*/
CREATE TABLE cliente (
    cliente_id                          INTEGER     NOT NULL 
                                        CONSTRAINT  cliente_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    identificacion                      TEXT        NOT NULL,
    nombre                              TEXT        NOT NULL,
    tipo                                TEXT        NOT NULL DEFAULT 'persona física',
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    correo_electronico                  TEXT            NULL,
    telefono                            TEXT            NULL,
    lugar_id                            INTEGER     NOT NULL,
    CONSTRAINT cliente_uq_identificacion UNIQUE (identificacion),
    CONSTRAINT cliente_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT cliente_ck_tipo CHECK ( tipo IN ('persona física', 'persona física')),
    CONSTRAINT cliente_fk_lugar_id FOREIGN KEY (lugar_id) 
        REFERENCES lugar
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(cliente);

PRAGMA ignore_check_constraints = 1;
insert into cliente (cliente_id, identificacion, nombre, lugar_id) values (1000,'00-0000-0000','Cliente general',1000);
PRAGMA ignore_check_constraints = 0;


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER cliente_on_delete
    BEFORE DELETE ON cliente
    BEGIN
        UPDATE cliente SET estado = 'eliminado' WHERE cliente_id = old.cliente_id;
        SELECT (RAISE(IGNORE));
    END;


/*
EN ESTA TABLA SE REGISTRA LA INFORMACION DEL PROVEEDOR,
TIENE UN PROVEEDOR POR GENERICO EN CASO DE DESCONOCER EL PROVEEDOR O
NO NOS INTERESA REGISTRAR UN PROVEEDOR ESPECIFICO
*/
CREATE TABLE proveedor (
    proveedor_id                        INTEGER     NOT NULL 
                                        CONSTRAINT  proveedor_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    identificacion                      TEXT        NOT NULL,
    nombre                              TEXT        NOT NULL,
    tipo                                TEXT        NOT NULL DEFAULT 'persona física',
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    correo_electronico                  TEXT            NULL,
    telefono                            TEXT            NULL,
    lugar_id                            INTEGER     NOT NULL,
    CONSTRAINT proveedor_uq_identificacion UNIQUE (identificacion),
    CONSTRAINT proveedor_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT proveedor_ck_tipo CHECK ( tipo IN ('persona física', 'persona física')),
    CONSTRAINT proveedor_fk_lugar_id FOREIGN KEY (lugar_id) 
        REFERENCES lugar
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(proveedor);
PRAGMA ignore_check_constraints = 1;
insert into proveedor (proveedor_id, identificacion, nombre, lugar_id) values (1000,'00-0000-0000','Proveedor general',1000);
PRAGMA ignore_check_constraints = 0;


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER proveedor_on_delete
    BEFORE DELETE ON proveedor
    BEGIN
        UPDATE proveedor SET estado = 'eliminado' WHERE proveedor_id = old.proveedor_id;
        SELECT (RAISE(IGNORE));
    END;


/*
ESTA TABLA ES PARA REGISTAR PRODUCTOS, HAY CAMPOS QUE TIENEN COMENTARIOS ESPECIALES
POR FAVOR REVISARLOS
SI LA EMPRESA TIENE PRODUCTO PERECEDERO, SE DEBE USAR EN CONJUNTO CON LA TABLA DE PRODUCTO_LOTE
*/
CREATE TABLE producto (
    producto_id                         INTEGER     NOT NULL 
                                        CONSTRAINT  producto_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    sku                                 TEXT        NOT NULL,
    nombre                              TEXT        NOT NULL,
    fecha_registro                      DATE        NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    costo_unitario                      REAL        NOT NULL DEFAULT 0,
    porcentaje_impuesto                 REAL        NOT NULL DEFAULT 0,        -- PORCENTAJE DE IMPUESTOS PARA CALCULAR EL MONTO
    monto_impuesto                      REAL        NOT NULL DEFAULT 0,        -- PARA EVITAR ESTAR CALCULAR EL MONTO CON EL PORCENTAJE
    monto_utilidad                      REAL        NOT NULL DEFAULT 0,
    precio                              REAL        NOT NULL DEFAULT 0,
    redondeo                            INTEGER     NOT NULL DEFAULT 0,        -- SI LA EMPRESA NO REDONDEA DEJAR EN 0
    precio_final                        INTEGER     NOT NULL DEFAULT 0,        -- SI LA EMPRESA REDONDEA PONERLO ACÁ, SINO COPIAR EN ESTE CAMPO EL VALOR DEL PRECIO
    cantidad                            REAL        NOT NULL DEFAULT 0,        -- DISPONIBLE + RESEVADOR DEBERIA SUMAR ESTE NUMERO
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    disponible                          REAL        NOT NULL DEFAULT 0,
    reservado                           REAL        NOT NULL DEFAULT 0,
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    dias_vida_util                      INTEGER         NULL ,                 -- SI NO TIENE VENCIMIENTO DEJAR EN NULL
    CONSTRAINT producto_uq_sku UNIQUE (sku),
    CONSTRAINT producto_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT producto_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm'))
);
PRAGMA foreign_key_list(producto);

/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER producto_on_delete
    BEFORE DELETE ON producto
    BEGIN
        UPDATE producto SET estado = 'eliminado' WHERE producto_id = old.producto_id;
        SELECT (RAISE(IGNORE));
    END;


/*
SI LA EMPRESA TIENE PRODUCTO PERECEDERO DEBE REGISTRAR LOS PRODUCTOS ACA
EL TOTAL DE UN MISMO PRODUCTO DEBERIA DE ACUMULARSE Y MOSTRARSE EN LA TABLA PRODUCTO
*/
CREATE TABLE producto_lote (
    producto_lote_id                    INTEGER     NOT NULL 
                                        CONSTRAINT  producto_lote_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    producto_id                         INTEGER     NOT NULL,
    fecha_ingreso                       DATE        NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    cantidad                            REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    fecha_caducidad                     DATE            NULL ,                 -- SI TIENE VENCIMIENTO PONER FECHA, SINO DEJAR EN NULL
    CONSTRAINT producto_lote_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT producto_lote_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(producto_lote);


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER producto_lote_on_delete
    BEFORE DELETE ON producto_lote
    BEGIN
        UPDATE producto_lote SET estado = 'eliminado' WHERE producto_lote_id = old.producto_lote_id;
        SELECT (RAISE(IGNORE));
    END;


/*
ESTA TABLA ES PARA REGISTAR VENTAS PARA USAR PARA ANALISIS DE PRONOSTICOS
LOS CAMPUS NULL SON OPCIONALES, ESTA DISEÑADA PARA USARSE EN DIFERENTES
CONFIGURACIONES
*/
CREATE TABLE venta (
    venta_id                            INTEGER     NOT NULL 
                                        CONSTRAINT  materia_prima_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    fecha                               DATE        NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    cantidad_vendida                    REAL        NOT NULL,
    monto_total                         REAL        NOT NULL,
    cliente_id                          INTEGER         NULL,
    local_id                            INTEGER         NULL,
    lugar_id                            INTEGER         NULL,
    costo_unitario                      REAL            NULL,
    utilidad_unitaria                   REAL            NULL,
    impuesto_unitario                   REAL            NULL,
    CONSTRAINT venta_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT venta_fk_cliente_id FOREIGN KEY (cliente_id) 
        REFERENCES cliente
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT venta_fk_local_id FOREIGN KEY (local_id) 
        REFERENCES local
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT venta_fk_lugar_id FOREIGN KEY (lugar_id) 
        REFERENCES lugar
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(venta);


/*
EN ESTA TABLA DEBE REGISTRAR LA INFORMACION GENERAL DE LA MATERIA PRIMA
AL IGUAL QUE PRODUCTO EXITE MATERIA PRIMA QUE ES PERECEDERO, EN ESTE CASO
DEBE TRABAJAR CON MATERIA_PRIMA_LOTE 
*/
CREATE TABLE materia_prima (
    materia_prima_id                    INTEGER     NOT NULL 
                                        CONSTRAINT  materia_prima_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    sku                                 TEXT        NOT NULL,
    nombre                              TEXT        NOT NULL,
    fecha_registro                      DATE        NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    costo_unitario                      REAL        NOT NULL DEFAULT 0,
    cantidad                            REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    reservado                           REAL        NOT NULL DEFAULT 0,
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    dias_vida_util                      INTEGER         NULL,                  -- SI NO TIENE VENCIMIENTO DEJAR EN NULL
    CONSTRAINT materia_prima_uq_sku UNIQUE (sku),
    CONSTRAINT materia_prima_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT materia_prima_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm'))
);
PRAGMA foreign_key_list(materia_prima);


/*
EN ESTA TABLA DEBE REGISTRAR LA INFORMACION GENERAL DE LA MATERIA PRIMA
Y LOS PROVEEDORES. ASOCIANDO LA INFORMACION QUE NACE DE LA RELACION DE LOS
DOS ELEMENTOS, COMO ES EL COSTO, CANTIDAD MINIMA DE ENTREGA Y TIEMPO DE ENTREGA
*/
CREATE TABLE materia_prima_proveedor (
    materia_prima_proveedor_id          INTEGER     NOT NULL 
                                        CONSTRAINT  materia_prima_proveedor_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    materia_prima_id                    INTEGER     NOT NULL,
    proveedor_id                        INTEGER     NOT NULL,
    costo                               REAL        NOT NULL,
    codigo_proveedor                    TEXT            NULL,
    cantidad_venta                      REAL        NOT NULL DEFAULT 0,
    unidad_venta                        TEXT        NOT NULL DEFAULT 'unidad',
    cantidad_minima_pedido              REAL        NOT NULL DEFAULT 1,
    pedidos_en_multiplos                REAL        NOT NULL DEFAULT 1,
    tiempo_entrega                      REAL        NOT NULL DEFAULT 1,
    tiempo_entrega_unidad               REAL        NOT NULL DEFAULT 'días',
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    CONSTRAINT materia_prima_proveedor_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT materia_prima_proveedor_ck_unidad_venta CHECK ( unidad_venta IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT materia_prima_proveedor_ck_tiempo_entrega_unidad CHECK ( tiempo_entrega_unidad IN ('días', 'semanas','meses')),
    CONSTRAINT materia_prima_proveedor_fk_materia_prima_id FOREIGN KEY (materia_prima_id) 
        REFERENCES materia_prima
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT materia_prima_proveedor_fk_proveedor_id FOREIGN KEY (proveedor_id) 
        REFERENCES proveedor
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(materia_prima_proveedor);


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER materia_prima_on_delete
    BEFORE DELETE ON materia_prima
    BEGIN
        UPDATE materia_prima SET estado = 'eliminado' WHERE materia_prima_id = old.materia_prima_id;
        SELECT (RAISE(IGNORE));
    END;


/*
SI LA EMPRESA TIENE PRODUCTO PERECEDERO DEBE REGISTRAR LOS PRODUCTOS ACA
EL TOTAL DE UN MISMO PRODUCTO DEBERIA DE ACUMULARSE Y MOSTRARSE EN LA TABLA PRODUCTO
*/
CREATE TABLE materia_prima_lote (
    materia_prima_lote_id               INTEGER     NOT NULL 
                                        CONSTRAINT  materia_prima_lote_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    materia_prima_id                    INTEGER     NOT NULL,
    fecha_ingreso                       DATE        NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    cantidad                            REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    fecha_caducidad                     DATE            NULL ,                 -- SI TIENE VENCIMIENTO PONER FECHA, SINO DEJAR EN NULL
    CONSTRAINT materia_prima_lote_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado')),
    CONSTRAINT materia_prima_lote_fk_materia_prima_id FOREIGN KEY (materia_prima_id) 
        REFERENCES materia_prima
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(materia_prima_lote);


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER materia_prima_lote_on_delete
    BEFORE DELETE ON materia_prima_lote
    BEGIN
        UPDATE materia_prima_lote SET estado = 'eliminado' WHERE materia_prima_lote_id = old.materia_prima_lote_id;
        SELECT (RAISE(IGNORE));
    END;


/*
EN ESTA TABLA SE REGISTRA LA INFORMACION DEL BILL OF MATERIAL
PERMITE EL REGISTRO DE MULTIPLES RECETAS PARA UN PRODUCTO, 
PERO SOLO UNA A A VEZ ESTA ACTIVA, LA QUE ESTA MARCADA COMO RECETA PRINCIPAL
SI LA EMPRESA SOLO USA UNA RECETA, SOLO SE REGISTRA UNA
*/
CREATE TABLE bom (
    bom_id                              INTEGER     NOT NULL 
                                        CONSTRAINT  bom_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    producto_id                         INTEGER     NOT NULL,
    version                             TEXT        NOT NULL DEFAULT 1,
    receta_principal                    BOOLEAN     NOT NULL DEFAULT 1,
    comentario                          TEXT        NOT NULL DEFAULT '',
    costo_acumulado_componentes         REAL        NOT NULL DEFAULT 0,        -- SE DEBERIA DE SUMAR EL COSTO DE TODOS LOS COMPONENTES
    costo_acumulado_materia_prima       REAL        NOT NULL DEFAULT 0,        -- SE DEBERIA DE SUMAR TODA LA MATERIA PRIMA DIRECTA
    costo_operativos                    REAL        NOT NULL DEFAULT 0,        -- COLOCAR EL COSTO DIRECTO DE FABRICACION
    costo_total                         REAL        NOT NULL DEFAULT 0,        -- SERIA IMPORTANTE REVISA ESTE COSTO CON EL COSTO REGISTRADO EN PRODUCTO
    tiempo_fabricacion                  REAL        NOT NULL DEFAULT 0,        -- TIEMPO DE FABRICACION POR UNIDAD PARA ANALISIS RAPIDOS DE CRP
    fecha_registro                      DATE        NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    estado                              TEXT        NOT NULL DEFAULT 'activo',
    CONSTRAINT bom_componentes_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT bom_uq_version UNIQUE (producto_id, version),
    CONSTRAINT bom_ck_estado CHECK ( estado IN ('activo', 'inactivo', 'eliminado'))
);
PRAGMA foreign_key_list(bom);


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN DELETE EN
LA BASE DE DATOS, DETIENE LA OPERACION Y LO QUE HACE ES PONER EL DATO COMO 'ELIMINADO'
PARA EVITAR INCONSISTENCIAS EN LA INTEGRIDAD REFERENCIAL
*/
CREATE TRIGGER bom_on_delete
    BEFORE DELETE ON bom
    BEGIN
        UPDATE bom SET estado = 'eliminado' WHERE bom_id = old.bom_id;
        SELECT (RAISE(IGNORE));
    END;
    
    
/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN INSERT EN
LA BASE DE DATOS, APLICA UNA OPERACION ADICIONAL,
ACTUALIZAR EL VALOR VERSION DEFAULT PARA SOLO EXISTA UNA VERSION PRINCIPAL
*/
CREATE TRIGGER bom_on_insert
    AFTER INSERT ON bom
    BEGIN
        UPDATE bom SET receta_principal = 0 
        where 
            bom_id <> new.bom_id
            AND
            producto_id = new.producto_id
            AND
            EXISTS (select * from bom where bom_id = new.bom_id and receta_principal = 1 and new.estado = 'activo');
       
    END;


/*
ESTE CODIGO SE EJECUTA EN AUTOMATICO, EN CASO QUE SE INTENTE APLICAR UN UPDATE EN
LA BASE DE DATOS, APLICA UNA OPERACION ADICIONAL,
ACTUALIZAR EL VALOR VERSION DEFAULT PARA SOLO EXISTA UNA VERSION PRINCIPAL
*/
CREATE TRIGGER bom_on_update
    AFTER UPDATE ON bom
    BEGIN
        UPDATE bom SET receta_principal = 0 
        where 
            bom_id <> new.bom_id
            AND
            producto_id = new.producto_id
            AND
            EXISTS (select * from bom where bom_id = new.bom_id and receta_principal = 1 and new.estado = 'activo');
       
    END;


/*
EN ESTA TABLA SE REGISTRA LA INFORMACION DE LOS COMPONENTES DEL BILL OF MATERIAL
LOS COMPONENTES SON PRODUCTOS TAMBIEN, DEBIDO A QUE SON FABRICADOS POR LA EMPRESA
*/
CREATE TABLE bom_componente (
    bom_componente_id                   INTEGER     NOT NULL 
                                        CONSTRAINT  bom_componentes_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    bom_id                              INTEGER     NOT NULL,
    componente_id                       INTEGER     NOT NULL,
    cantidad                            REAL        NOT NULL,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    costo_unitario                      REAL        NOT NULL DEFAULT 0,
    tiempo_fabricacion                  REAL        NOT NULL DEFAULT 1,
    tiempo_fabricacion_unidad           REAL        NOT NULL DEFAULT 'días',
    CONSTRAINT bom_componente_fk_bom_id FOREIGN KEY (bom_id) 
        REFERENCES bom
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT bom_componente_fk_componente_id FOREIGN KEY (componente_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT bom_componente_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT bom_componente_ck_tiempo_fabricacion_unidad CHECK ( tiempo_fabricacion_unidad IN ('días', 'semanas','meses'))
);
PRAGMA foreign_key_list(bom_componente);


/*
EN ESTA TABLA SE REGISTRA LA INFORMACION DE LAS MATERIAS PRIMAS DEL BILL OF MATERIAL
*/
CREATE TABLE bom_materia_prima (
    bom_materia_prima_id                INTEGER     NOT NULL 
                                        CONSTRAINT  bom_materias_primas_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    bom_id                              INTEGER     NOT NULL,
    materia_prima_id                    INTEGER     NOT NULL,
    cantidad                            REAL        NOT NULL,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    costo                               REAL        NOT NULL DEFAULT 0,
    tiempo_fabricacion                  REAL        NOT NULL DEFAULT 1,
    tiempo_fabricacion_unidad           REAL        NOT NULL DEFAULT 'días',
    CONSTRAINT bom_materia_prima_fk_bom_id FOREIGN KEY (bom_id) 
        REFERENCES bom
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT bom_materia_prima_fk_materia_prima_id FOREIGN KEY (materia_prima_id) 
        REFERENCES materia_prima
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT bom_materia_prima_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT bom_materia_prima_ck_tiempo_fabricacion_unidad CHECK ( tiempo_fabricacion_unidad IN ('días', 'semanas','meses'))
);
PRAGMA foreign_key_list(bom_materia_prima);


/*
PARA EL CALCULO BASICO DE CAPACIDAD SE USA MINUTOS POR DIA, ESTA TABLA LLEVA ESE REGISTRO
*/
CREATE TABLE capacidad_diaria (
    capacidad_diaria_id                 INTEGER     NOT NULL 
                                        CONSTRAINT  capacidad_diaria_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    fecha                               DATE        NOT NULL,
    cantidad_minutos_totales            INTEGER     NOT NULL DEFAULT 1,
    cantidad_minutos_reservados         INTEGER     NOT NULL DEFAULT 0,
    cantidad_minutos_disponibles        INTEGER     NOT NULL DEFAULT 0,
    CONSTRAINT capacidad_diaria_uq_fecha UNIQUE (fecha)
);

/*
PARA INICIAR UN PLAN DE PRODUCCION SE DEBEN ASOCIAR LOS PRODUCTOS QUE SE EVALUARAN EN CONJUNTO
EN MPS Y MRP, ESTA TABLA CREA EL CONJUNTO CON EL QUE SE HARA TODO EL ANALISIS.
EL ESTADO FUNCIONA COMO UN FLUJO DE TRABAJO PARA DETERMINAR LAS ETAPAS DEL PROCESO DE CALCULO
*/
CREATE TABLE plan_produccion (
    plan_produccion_id                  INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    nombre                              TEXT        NOT NULL,
    fecha_registro                      DATE        NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    fecha_inicio_produccion             DATE            NULL,
    cantidad_periodo                    INTEGER     NOT NULL DEFAULT 1,
    tipo_periodo                        TEXT        NOT NULL DEFAULT 'día',
    estado                              TEXT        NOT NULL DEFAULT 'registrado',
    CONSTRAINT plan_produccion_uq_nombre UNIQUE (nombre),
    CONSTRAINT plan_produccion_ck_estado CHECK (estado IN ('registrado', 'aprobado', 'finalizado', 'cancelado')),
    CONSTRAINT plan_produccion_ck_tipo_periodo CHECK (tipo_periodo IN ('día', 'semana','mes','año'))
);

/*
ESTA TABLA CONTIENE LA INFORMACIÓN DE LOS PRODUCTOS QUE SE VAN A EVALUAR EN ESTE PLAN DE PRODUCCION
PARA CADA UNO SE PONE EL INVENTARIO INICIAL Y COMO SE CALCULO (SI ES CANTIDAD ABSOLUTA O PORCENTUAL)
*/
CREATE TABLE plan_produccion_producto (
    plan_produccion_producto_id         INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_producto_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    inv_inicial                         REAL        NOT NULL DEFAULT 0,
    inv_seguridad                       REAL        NOT NULL DEFAULT 0,
    inv_seguridad_tipo                  TEXT        NOT NULL DEFAULT 'unidades',
    porc_inv_seguridad                  REAL            NULL DEFAULT null,
    multiplos_pedido                    REAL        NOT NULL DEFAULT 1,
    CONSTRAINT plan_produccion_producto_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_ck_inv_seguridad_tipo CHECK ( inv_seguridad_tipo IN ('unidades', 'porcentaje'))
);
PRAGMA foreign_key_list(plan_produccion_producto);


/*
EN ESTA TABLA SE REGISTRAN LOS DESPACHO QUE SE VAN A UTILIZAR, LAS FECHAS SON LOS LIMITES DEL PERIODO
DEBEN COINCIDIR CON EL TIPO DE PERIODO DEL REGISTRO INICIAL
*/
CREATE TABLE plan_produccion_producto_despacho (
    plan_produccion_producto_despacho_id INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_producto_despacho_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    fecha_inicio                        DATE        NOT NULL,                  -- ESTA FECHA INCLUYE EL VALOR
    fecha_final                         DATE        NOT NULL,                  -- ESTA FECHA LIMITE NO INCLUYENTE
    cantidad                            REAL        NOT NULL DEFAULT 0,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    CONSTRAINT plan_produccion_producto_despacho_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_produccion_producto_despacho_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_despacho_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm'))
);
PRAGMA foreign_key_list(plan_produccion_producto_despacho);


/*
DEBIDO A QUE SE GENERA UNA SOLUCION Y SE EVALUA HASTA ENCONTRAR LA ADECUADA, EL SISTEMA PUEDE GENERAR MULTIPLES
ESCENARIOS RESOLUTIVOS, ACA SE HACE EL GRUPO DE ESCENARIOS
*/
CREATE TABLE plan_produccion_escenario (
    plan_produccion_escenario_id        INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_escenario_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    numero_escario_del_plan_produccion  INTEGER     NOT NULL,
    estado                              TEXT        NOT NULL DEFAULT 'en construcción',
    CONSTRAINT plan_produccion_escenario_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
PRAGMA foreign_key_list(plan_produccion_escenario);


CREATE TABLE plan_produccion_producto_mps (
    plan_produccion_producto_mps_id     INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_producto_mps_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_escenario_id        INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    fecha_inicio                        DATE        NOT NULL,
    fecha_final                         DATE        NOT NULL,
    tipo                                TEXT        NOT NULL DEFAULT 'perseguidor',
    CONSTRAINT plan_produccion_producto_mps_fk_plan_produccion_escenario_id FOREIGN KEY (plan_produccion_escenario_id) 
        REFERENCES plan_produccion_escenario
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_mps_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_mps_ck_tipo CHECK ( tipo IN ('perseguidor', 'nivelado', 'mixto'))
);
PRAGMA foreign_key_list(plan_produccion_producto_mps);


CREATE TABLE plan_produccion_producto_mps_periodo (
    plan_produccion_producto_mps_periodo_id INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_producto_mps_periodo_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    producto_id                         INTEGER     NOT NULL,
    plan_produccion_producto_mps_id     INTEGER     NOT NULL,
    fecha                               DATE        NOT NULL,
    inv_inicial                         REAL        NOT NULL DEFAULT 0,
    plan_produccion                     REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    despacho                            REAL        NOT NULL DEFAULT 0,
    inv_final                           REAL        NOT NULL DEFAULT 0,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    CONSTRAINT plan_produccion_producto_mps_periodo_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_mps_periodo_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT plan_produccion_producto_mps_periodo_fk_plan_produccion_producto_mps_id FOREIGN KEY (plan_produccion_producto_mps_id) 
        REFERENCES plan_produccion_producto_mps
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(plan_produccion_producto_mps_periodo);


CREATE TABLE plan_produccion_producto_mrp (
    plan_produccion_producto_mrp_id     INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_producto_mrp_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    plan_produccion_producto_mps_id     INTEGER     NOT NULL,
    fecha_inicio                        DATE        NOT NULL,
    fecha_final                         DATE        NOT NULL,
    tipo                                TEXT        NOT NULL DEFAULT 'perseguidor',
    evaluacion                          REAL        NOT NULL,
    seleccionado                        INT         NOT NULL,
    CONSTRAINT plan_produccion_producto_mps_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_mps_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_produccion_producto_mps_ck_tipo CHECK ( tipo IN ('perseguidor', 'nivelado', 'nivelado_por_componentes', 'otro')),
    CONSTRAINT plan_produccion_producto_mps_periodo_fk_plan_produccion_producto_mps_id FOREIGN KEY (plan_produccion_producto_mps_id) 
        REFERENCES plan_produccion_producto_mps
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
PRAGMA foreign_key_list(plan_produccion_producto_mrp);


CREATE TABLE plan_producc_prod_mpr_compte (
    plan_producc_prod_mpr_compte_id INTEGER     NOT NULL 
                                        CONSTRAINT  plan_producc_prod_mpr_compte_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    plan_produccion_producto_mrp_id     INTEGER     NOT NULL,
    fecha                               DATE        NOT NULL,
    inv_inicial                         REAL        NOT NULL DEFAULT 0,
    plan_compras                        REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    inv_seguridad                       REAL        NOT NULL DEFAULT 0,
    despacho                            REAL        NOT NULL DEFAULT 0,
    inv_final                           REAL        NOT NULL DEFAULT 0,
    pedido                              REAL        NOT NULL DEFAULT 0,
    pedido_ajustado                     REAL        NOT NULL DEFAULT 0,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    nivel                               INTEGER     NOT NULL DEFAULT 1,
    procesado                           INTEGER     NOT NULL DEFAULT 0,
    acumulado                           INTEGER     NOT NULL DEFAULT 0,
    raiz                                INTEGER         NULL,
    padre                               INTEGER         NULL,
    CONSTRAINT plan_producc_prod_mpr_compte_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_producc_prod_mpr_compte_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_producc_prod_mpr_compte_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT plan_producc_prod_mpr_compte_fk_raiz FOREIGN KEY (raiz) 
        REFERENCES plan_producc_prod_mpr_compte_perseguidor
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_producc_prod_mpr_compte_fk_padre FOREIGN KEY (padre) 
        REFERENCES plan_producc_prod_mpr_compte_perseguidor
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT plan_producc_prod_mpr_compte_fk_plan_produccion_producto_mrp_id FOREIGN KEY (plan_produccion_producto_mrp_id) 
        REFERENCES plan_produccion_producto_mrp
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
PRAGMA foreign_key_list(plan_producc_prod_mpr_compte);


CREATE TABLE plan_produccion_producto_mpr_matprima (
    plan_produccion_producto_mpr_matprima_id INTEGER     NOT NULL 
                                        CONSTRAINT  plan_produccion_producto_mpr_matprima_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    plan_produccion_producto_mrp_id     INTEGER     NOT NULL,
    fecha                               DATE        NOT NULL,
    inv_inicial                         REAL        NOT NULL DEFAULT 0,
    plan_compras                        REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    inv_seguridad                       REAL        NOT NULL DEFAULT 0,
    despacho                            REAL        NOT NULL DEFAULT 0,
    inv_final                           REAL        NOT NULL DEFAULT 0,
    pedido                              REAL        NOT NULL DEFAULT 0,
    pedido_ajustado                     REAL        NOT NULL DEFAULT 0,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    nivel                               INTEGER     NOT NULL DEFAULT 1,
    procesado                           INTEGER     NOT NULL DEFAULT 0,
    acumulado                           INTEGER     NOT NULL DEFAULT 0,
    CONSTRAINT plan_produccion_producto_mpr_matprima_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_produccion_producto_mpr_matprima_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_produccion_producto_mpr_matprima_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT plan_produccion_producto_mpr_matprima_fk_plan_produccion_producto_mrp_id FOREIGN KEY (plan_produccion_producto_mrp_id) 
        REFERENCES plan_produccion_producto_mrp
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
PRAGMA foreign_key_list(plan_produccion_producto_mpr_matprima);


CREATE TABLE plan_producc_prod_mpr_comp_final (
    plan_producc_prod_mpr_comp_final_id INTEGER     NOT NULL 
                                        CONSTRAINT  pplan_producc_prod_mpr_comp_final_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    plan_produccion_producto_mrp_id     INTEGER     NOT NULL,
    fecha                               DATE        NOT NULL,
    inv_inicial                         REAL        NOT NULL DEFAULT 0,
    plan_compras                        REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    inv_seguridad                       REAL        NOT NULL DEFAULT 0,
    despacho                            REAL        NOT NULL DEFAULT 0,
    inv_final                           REAL        NOT NULL DEFAULT 0,
    pedido                              REAL        NOT NULL DEFAULT 0,
    pedido_ajustado                     REAL        NOT NULL DEFAULT 0,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    CONSTRAINT plan_producc_prod_mpr_comp_final_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_producc_prod_mpr_comp_final_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_producc_prod_mpr_comp_final_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT plan_producc_prod_mpr_comp_final_fk_plan_produccion_producto_mrp_id FOREIGN KEY (plan_produccion_producto_mrp_id) 
        REFERENCES plan_produccion_producto_mrp
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
PRAGMA foreign_key_list(plan_producc_prod_mpr_comp_final);


CREATE TABLE plan_producc_prod_mpr_matprima_final (
    plan_producc_prod_mpr_matprima_final_id INTEGER NOT NULL 
                                        CONSTRAINT  plan_producc_prod_mpr_matprima_final_pk 
                                        PRIMARY KEY AUTOINCREMENT,
    plan_produccion_id                  INTEGER     NOT NULL,
    producto_id                         INTEGER     NOT NULL,
    plan_produccion_producto_mrp_id     INTEGER     NOT NULL,
    fecha                               DATE        NOT NULL,
    inv_inicial                         REAL        NOT NULL DEFAULT 0,
    plan_compras                        REAL        NOT NULL DEFAULT 0,
    disponible                          REAL        NOT NULL DEFAULT 0,
    inv_seguridad                       REAL        NOT NULL DEFAULT 0,
    despacho                            REAL        NOT NULL DEFAULT 0,
    inv_final                           REAL        NOT NULL DEFAULT 0,
    pedido                              REAL        NOT NULL DEFAULT 0,
    pedido_ajustado                     REAL        NOT NULL DEFAULT 0,
    unidad                              TEXT        NOT NULL DEFAULT 'unidad',
    CONSTRAINT plan_producc_prod_mpr_matprima_final_fk_plan_produccion_id FOREIGN KEY (plan_produccion_id) 
        REFERENCES plan_produccion
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_producc_prod_mpr_matprima_final_fk_producto_id FOREIGN KEY (producto_id) 
        REFERENCES producto
        ON UPDATE CASCADE
        ON DELETE NO ACTION,
    CONSTRAINT plan_producc_prod_mpr_matprima_final_ck_unidad CHECK ( unidad IN ('unidad', 'gramos', 'cc', 'cm')),
    CONSTRAINT plan_producc_prod_mpr_matprima_final_fk_plan_produccion_producto_mrp_id FOREIGN KEY (plan_produccion_producto_mrp_id) 
        REFERENCES plan_produccion_producto_mrp
        ON UPDATE CASCADE
        ON DELETE NO ACTION
);
PRAGMA foreign_key_list(plan_producc_prod_mpr_matprima_final);
          '''
    conn.executescript(sql)

def carga_datos_prueba(conn = None):
    sql = '''
PRAGMA ignore_check_constraints = 1;
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (1,'P01','Vehículo Deportivo','2023-01-01','2023-01-01',1000,'unidad',62500,50000,100,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (2,'P02','Vehículo Familiar','2023-01-01','2023-01-01',700,'unidad',100000,80000,40,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (3,'P03','Vehículo Sedán','2023-01-01','2023-01-01',3400,'unidad',50000,40000,340,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (4,'P04','Motor Sencillo','2023-01-01','2023-01-01',0,'unidad',2500,2000,0,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (5,'P05','Motor Alto Rendimiento','2023-01-01','2023-01-01',10,'unidad',4375,3500,50,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (6,'P06','Puerta delantera sencilla','2023-01-01','2023-01-01',12,'unidad',2437,1950,53,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (7,'P07','Puerta trasera sencilla','2023-01-01','2023-01-01',12,'unidad',2437,1950,53,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (8,'P08','Puerta delantera deportiva','2023-01-01','2023-01-01',12,'unidad',3687,2950,53,0,'activo');
insert into producto (producto_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (9,'P09','Block de motor','2023-01-01','2023-01-01',7,'unidad',1250,1000,32,0,'activo');
insert into materia_prima (materia_prima_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (1,'M01','Llanta','2023-01-01','2023-01-01',4000,'unidad',1300,1000,100,0,'activo');
insert into materia_prima (materia_prima_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (2,'M02','Tornillos','2023-01-01','2023-01-01',70340,'unidad',130,100,4034,0,'activo');
insert into materia_prima (materia_prima_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (3,'M03','Lamina metal','2023-01-01','2023-01-01',33400,'unidad',650,500,3240,0,'activo');
insert into materia_prima (materia_prima_id,sku,nombre,fecha_registro,fecha_ultimo_registro,cantidad,unidad,precio,costo_unitario,disponible,reservado,estado) values (4,'M04','Ventana','2023-01-01','2023-01-01',30,'unidad',780,600,0,0,'activo');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (1,1,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (2,2,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (3,3,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (4,4,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (5,5,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (6,6,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (7,7,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (8,8,'Principal',1,'Datos de prueba');
INSERT INTO bom (bom_id,producto_id,version,version_default,comentario) VALUES  (9,9,'Principal',1,'Datos de prueba');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (1,1,5,1,'unidad',0,2,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (1,1,8,2,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,2,4,1,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,2,6,2,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,2,7,2,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,3,4,1,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,3,6,2,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,3,7,2,'unidad',0,1,'días');
insert into bom_componente (bom_id, producto_id,componente_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (4,4,9,1,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (1,1,1,1,4,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (1,2,1,2,2000,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (1,3,1,3,200,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (1,4,1,4,4,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,5,2,1,4,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,6,2,2,3000,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,7,2,3,300,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (2,8,2,4,5,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,9,3,1,4,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,10,3,2,3200,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,11,3,3,350,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (3,12,3,4,5,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (4,13,4,2,200,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (5,14,5,2,220,'unidad',0,0,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (6,15,6,4,1,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (7,16,7,4,1,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (8,17,8,4,1,'unidad',0,1,'días');
insert into bom_materia_prima (bom_id, bom_materias_primas_id,producto_id,materia_prima_id,cantidad,unidad,costo,lead_time,lead_time_unidad) values (9,18,9,2,16,'unidad',0,0,'días');


INSERT INTO proyecto (proyecto_id, nombre) values (1,'Prueba de proyecto');

INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(1,1,1,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(2,1,2,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(3,1,3,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(4,1,4,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(5,1,5,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(6,1,6,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(7,1,7,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(8,1,8,0.0,0.0,'unidades',NULL,1.0);
INSERT INTO proyecto_producto (proyecto_producto_id,proyecto_id,producto_id,inv_inicial,inv_seguridad,inv_seguridad_tipo,porc_inv_seguridad,multiplos_pedido) VALUES(9,1,9,0.0,0.0,'unidades',NULL,1.0);


INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(1,1,1,'2023-06-01 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(2,1,1,'2023-06-02 00:00:00.000',125.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(3,1,1,'2023-06-03 00:00:00.000',110.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(4,1,1,'2023-06-04 00:00:00.000',150.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(5,1,1,'2023-06-05 00:00:00.000',50.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(6,1,2,'2023-06-01 00:00:00.000',80.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(7,1,2,'2023-06-02 00:00:00.000',55.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(8,1,2,'2023-06-03 00:00:00.000',60.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(9,1,2,'2023-06-04 00:00:00.000',75.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(10,1,2,'2023-06-05 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(11,1,3,'2023-06-01 00:00:00.000',40.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(12,1,3,'2023-06-02 00:00:00.000',60.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(13,1,3,'2023-06-03 00:00:00.000',50.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(14,1,3,'2023-06-04 00:00:00.000',70.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(15,1,3,'2023-06-05 00:00:00.000',50.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(16,1,4,'2023-06-01 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(17,1,4,'2023-06-02 00:00:00.000',75.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(18,1,4,'2023-06-03 00:00:00.000',60.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(19,1,4,'2023-06-04 00:00:00.000',35.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(20,1,4,'2023-06-05 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(21,1,5,'2023-06-01 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(22,1,5,'2023-06-02 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(23,1,5,'2023-06-03 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(24,1,5,'2023-06-04 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(25,1,5,'2023-06-05 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(26,1,6,'2023-06-01 00:00:00.000',25.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(27,1,6,'2023-06-02 00:00:00.000',50.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(28,1,6,'2023-06-03 00:00:00.000',75.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(29,1,6,'2023-06-04 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(30,1,6,'2023-06-05 00:00:00.000',125.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(31,1,7,'2023-06-01 00:00:00.000',120.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(32,1,7,'2023-06-02 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(33,1,7,'2023-06-03 00:00:00.000',140.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(34,1,7,'2023-06-04 00:00:00.000',80.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(35,1,7,'2023-06-05 00:00:00.000',160.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(36,1,8,'2023-06-01 00:00:00.000',50.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(37,1,8,'2023-06-02 00:00:00.000',37.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(38,1,8,'2023-06-03 00:00:00.000',52.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(39,1,8,'2023-06-04 00:00:00.000',71.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(40,1,8,'2023-06-05 00:00:00.000',88.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(41,1,9,'2023-06-01 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(42,1,9,'2023-06-02 00:00:00.000',50.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(43,1,9,'2023-06-03 00:00:00.000',100.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(44,1,9,'2023-06-04 00:00:00.000',75.0,'unidad');
INSERT INTO proyecto_producto_despacho (proyecto_producto_despacho_id, proyecto_id,producto_id,fecha,cantidad,unidad) VALUES(45,1,9,'2023-06-05 00:00:00.000',150.0,'unidad');

PRAGMA ignore_check_constraints = 0;
        '''
    # TODO: Eliminado hasta no tener los cambios aplicados en la base de datos
    # conn.executescript(sql)



if '__main__' == __name__:
    conn = crear_conexion()
    if verificar_base_nueva(conn):
        crear_tablas(conn)
        carga_datos_prueba(conn)
    conn.close()