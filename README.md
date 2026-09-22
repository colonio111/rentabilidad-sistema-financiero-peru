# Rentabilidad de las cajas municipales frente a la banca múltiple en el Perú, 2015-2025

## Autora

**Lucía Pamela Colonio Yaringaño**  
**Código de matrícula:** 2024200495A  
**Tema N.º 12**

## Descripción del proyecto

Este proyecto analiza y compara la evolución de la rentabilidad de las cajas municipales y la banca múltiple en el sistema financiero peruano durante el periodo 2015-2025.

La rentabilidad será evaluada principalmente mediante los indicadores ROA y ROE. Además, se consideran variables relacionadas con el tamaño, la actividad crediticia y la calidad de la cartera.

## Pregunta de investigación

¿Cómo difiere la rentabilidad, medida a través del ROA y ROE, de las cajas municipales en comparación con la banca múltiple en el sistema financiero peruano durante el periodo 2015 a 2025?

## Objetivo

Analizar y comparar la evolución de la rentabilidad (ROA y ROE) entre las cajas municipales y la banca múltiple en el Perú durante el periodo 2015 a 2025, utilizando datos oficiales extraídos mediante programación.

## Fuente de datos

Los datos utilizados provienen de la **Superintendencia de Banca, Seguros y AFP (SBS)**.

La extracción se realiza mediante descarga programática de archivos oficiales publicados por la SBS.

El periodo establecido para la investigación es:

- Fecha de inicio: enero de 2015.
- Fecha de corte: diciembre de 2025.
- Frecuencia: mensual.

## Variables del estudio

La base procesada está compuesta por las siguientes variables:

- `fecha`: periodo mensual correspondiente a la observación.
- `tipo_institucion`: Banca Múltiple o Cajas Municipales.
- `roa`: rentabilidad sobre activos (%).
- `roe`: rentabilidad sobre patrimonio (%).
- `morosidad`: créditos atrasados respecto a créditos directos (%).
- `tamano_activo`: total de activos reportado por la SBS.
- `ratio_eficiencia_operativa`: gastos de operación respecto al margen financiero total (%).
- `margen_financiero_neto`: margen financiero neto reportado en el Estado de Ganancias y Pérdidas de la SBS.

## Extracción realizada

Actualmente se completó la descarga programática de los archivos oficiales de la SBS correspondientes al periodo enero de 2015 a diciembre de 2025.

Se obtuvieron:

- 132 periodos mensuales.
- 6 archivos oficiales por periodo.
- 792 archivos en total.
- 792 archivos validados correctamente.
- 792 archivos legibles.
- 0 archivos faltantes.
- 0 archivos con error de lectura.

Los archivos originales se conservan sin modificaciones en la carpeta local `datos_crudos/`.

## Base procesada

Se construyó una base preliminar con información mensual para Banca Múltiple y Cajas Municipales durante el periodo 2015-2025.

Resultados de la validación:

- 264 observaciones.
- 132 observaciones de Banca Múltiple.
- 132 observaciones de Cajas Municipales.
- 132 periodos mensuales.
- 8 columnas.
- 0 valores nulos.
- 0 filas duplicadas.
- 0 duplicados en la combinación de fecha y tipo de institución.

La base se encuentra en:

`datos procesados/base_procesada_2024200495A.csv`

Esta base corresponde a una primera construcción agregada por tipo de institución y podrá ser adaptada posteriormente de acuerdo con los requerimientos finales del trabajo.

## Estructura actual del proyecto

```text
COLONIO/

├── codigos/
│   ├── 01_extraccion_api.py
│   ├── 03_limpieza_datos.py
│   └── pruebas/
│       └── prueba.py
├── datos_crudos/
├── datos procesados/
│   └── base_procesada_2024200495A.csv
├── salidas/
├── log_ejecucion.txt
├── .gitignore
└── README.md