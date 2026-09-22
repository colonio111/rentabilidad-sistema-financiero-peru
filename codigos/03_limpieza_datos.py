# Autora: Colonio Yaringaño Lucía Pamela
# Código de matrícula: 2024200495A
# Tema N.º 12: Rentabilidad de las cajas municipales frente a la banca múltiple, 2015 a 2025
# Fecha de extracción: 2026-09-20

# ---------------------------------------------------------
# LIBRERÍAS
# ---------------------------------------------------------

import pandas as pd
from pathlib import Path
# ---------------------------------------------------------
# RUTAS DEL PROYECTO
# ---------------------------------------------------------

# Carpeta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Carpeta que contiene los archivos originales descargados de la SBS
RUTA_DATOS_CRUDOS = RUTA_PROYECTO / "datos_crudos"

# Carpeta donde se guardará la base procesada
RUTA_DATOS_PROCESADOS = RUTA_PROYECTO / "datos procesados"

# Crear la carpeta de datos procesados si no existe
RUTA_DATOS_PROCESADOS.mkdir(parents=True, exist_ok=True)
# ---------------------------------------------------------
# FUNCIÓN PARA LEER ARCHIVOS EXCEL DE LA SBS
# ---------------------------------------------------------

def leer_excel_sbs(ruta_archivo):
    """
    Lee un archivo Excel de la SBS utilizando el motor
    compatible con su formato interno.
    """
    try:
        return pd.read_excel(
            ruta_archivo,
            sheet_name=0,
            header=None,
            engine="xlrd"
        )

    except Exception:
        return pd.read_excel(
            ruta_archivo,
            sheet_name=0,
            header=None,
            engine="openpyxl"
        )
    # ---------------------------------------------------------
# FUNCIÓN PARA NORMALIZAR TEXTOS
# ---------------------------------------------------------

def normalizar_texto(valor):
    """
    Convierte un valor en texto uniforme para facilitar
    la búsqueda de etiquetas dentro de los archivos SBS.
    """
    return " ".join(
        str(valor)
        .replace("\n", " ")
        .strip()
        .upper()
        .split()
    )
# ---------------------------------------------------------
# FUNCIÓN PARA EXTRAER ROA Y ROE DE BANCA MÚLTIPLE
# ---------------------------------------------------------

def extraer_roa_roe_banca(ruta_archivo):
    """
    Extrae el ROA y ROE del total de la Banca Múltiple
    desde un archivo de indicadores financieros de la SBS.
    """

    # Leer el archivo Excel
    datos = leer_excel_sbs(ruta_archivo)

    # Buscar la columna correspondiente al Total Banca Múltiple
    columna_total = None

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if "TOTAL BANCA MÚLTIPLE" in texto:
                columna_total = columna
                break

        if columna_total is not None:
            break
    # Buscar las filas correspondientes al ROE, ROA y Morosidad 
    fila_roe = None
    fila_roa = None
    fila_morosidad = None

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if "UTILIDAD NETA ANUALIZADA / PATRIMONIO PROMEDIO" in texto:
                fila_roe = fila

            if "UTILIDAD NETA ANUALIZADA / ACTIVO PROMEDIO" in texto:
                fila_roa = fila
            if (
                "CRÉDITOS ATRASADOS" in texto
                and "CRÉDITOS DIRECTOS" in texto
                and "90 DÍAS" not in texto
                and " MN " not in f" {texto} "
                and " ME " not in f" {texto} "
            ):
                fila_morosidad = fila

    # Verificar que se hayan encontrado los datos necesarios
    if columna_total is None:
        raise ValueError("No se encontró la columna del Total Banca Múltiple.")

    if fila_roe is None:
        raise ValueError("No se encontró la fila correspondiente al ROE.")

    if fila_roa is None:
        raise ValueError("No se encontró la fila correspondiente al ROA.")

    if fila_morosidad is None:
        raise ValueError("No se encontró la fila correspondiente a la morosidad.")
    # Extraer los valores de ROA y ROE
    roe = datos.iloc[fila_roe, columna_total]
    roa = datos.iloc[fila_roa, columna_total]
    morosidad = datos.iloc[fila_morosidad, columna_total]

    # Devolver los resultados
    return roa, roe, morosidad

# ---------------------------------------------------------
# MESES UTILIZADOS EN LOS ARCHIVOS DE LA SBS
# ---------------------------------------------------------

MESES_SBS = {
    1: "en",
    2: "fe",
    3: "ma",
    4: "ab",
    5: "my",
    6: "jn",
    7: "jl",
    8: "ag",
    9: "se",
    10: "oc",
    11: "no",
    12: "di"
}

# ---------------------------------------------------------
# PRUEBA: BANCA MÚLTIPLE - DICIEMBRE 2025
# ---------------------------------------------------------

archivo_prueba = RUTA_DATOS_CRUDOS / "B-2401-di2025.XLS"

roa_banca, roe_banca, morosidad_banca = extraer_roa_roe_banca(archivo_prueba)

print("\nPRUEBA BANCA MÚLTIPLE - DICIEMBRE 2025")
print("ROA:", roa_banca)
print("ROE:", roe_banca)
print("Morosidad:", morosidad_banca)


# ---------------------------------------------------------
# FUNCIÓN PARA EXTRAER ROA Y ROE DE CAJAS MUNICIPALES
# ---------------------------------------------------------

def extraer_roa_roe_cajas(ruta_archivo):
    """
    Extrae el ROA y ROE del total de las Cajas Municipales
    desde un archivo de indicadores financieros de la SBS.
    """

    # Leer el archivo Excel
    datos = leer_excel_sbs(ruta_archivo)

    # Buscar la columna correspondiente al Total Cajas Municipales
    columna_total = None

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL CM":
                columna_total = columna
                break

        if columna_total is not None:
            break
    # Buscar las filas correspondientes al ROE y ROA
    fila_roe = None
    fila_roa = None
    fila_morosidad = None

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if "UTILIDAD NETA ANUALIZADA SOBRE PATRIMONIO PROMEDIO" in texto:
                fila_roe = fila

            if "UTILIDAD NETA ANUALIZADA SOBRE ACTIVO PROMEDIO" in texto:
                fila_roa = fila

            if (
                "CRÉDITOS ATRASADOS" in texto
                and "CRÉDITOS DIRECTOS" in texto
                and "90 DÍAS" not in texto
                and " MN " not in f" {texto} "
                and " ME " not in f" {texto} "
            ):
                fila_morosidad = fila
    # Verificar que se hayan encontrado los datos necesarios
    if columna_total is None:
        raise ValueError("No se encontró la columna del Total Cajas Municipales.")

    if fila_roe is None:
        raise ValueError("No se encontró la fila correspondiente al ROE.")

    if fila_roa is None:
        raise ValueError("No se encontró la fila correspondiente al ROA.")
    if fila_morosidad is None:
        raise ValueError("No se encontró la fila correspondiente a la morosidad.")
    
    
    

    # Extraer los valores de ROA, ROE y morosidad
    roe = datos.iloc[fila_roe, columna_total]
    roa = datos.iloc[fila_roa, columna_total]
    morosidad = datos.iloc[fila_morosidad, columna_total]

    # Devolver los resultados
    return roa, roe, morosidad

def extraer_activo_banca(ruta_archivo):
    """
    Extrae el total de activos de la Banca Múltiple
    desde el balance general publicado por la SBS.
    """
    datos = leer_excel_sbs(ruta_archivo)

    columna_total = None
    fila_activo = None

    # Buscar la columna correspondiente al Total Banca Múltiple
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL BANCA MÚLTIPLE":
                columna_total = columna
                break

        if columna_total is not None:
            break

    # Buscar la fila correspondiente al Total Activo
    for fila in range(datos.shape[0]):
        texto = normalizar_texto(datos.iloc[fila, columna_total])

        if texto == "TOTAL ACTIVO":
            fila_activo = fila
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Banca Múltiple."
        )

    if fila_activo is None:
        raise ValueError(
            "No se encontró la fila correspondiente al Total Activo."
        )

    activo_total = datos.iloc[fila_activo, columna_total]

    return activo_total

def extraer_activo_banca(ruta_archivo):
    """
    Extrae el total de activos de la Banca Múltiple
    desde el balance general publicado por la SBS.
    """
    datos = leer_excel_sbs(ruta_archivo)

    columna_total = None
    fila_activo = None

    # Buscar la columna del Total Banca Múltiple
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto.rstrip("*").strip() == "TOTAL BANCA MÚLTIPLE":
                columna_total = columna
                break

        if columna_total is not None:
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Banca Múltiple."
        )

    # Buscar la fila donde aparece TOTAL ACTIVO
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL ACTIVO":
                fila_activo = fila
                break

        if fila_activo is not None:
            break

    if fila_activo is None:
        raise ValueError(
            "No se encontró la fila correspondiente al Total Activo."
        )

    activo_total = datos.iloc[fila_activo, columna_total]

    return activo_total

    # Buscar TOTAL ACTIVO en la columna anterior
    columna_etiquetas = columna_total - 1

    for fila in range(datos.shape[0]):
        texto = normalizar_texto(
            datos.iloc[fila, columna_etiquetas]
        )

        if texto == "TOTAL ACTIVO":
            fila_activo = fila
            break

    if fila_activo is None:
        raise ValueError(
            "No se encontró la fila correspondiente al Total Activo."
        )

    activo_total = datos.iloc[fila_activo, columna_total]

    return activo_total

archivo_activo_banca = (
    RUTA_DATOS_CRUDOS / "B-2201-di2025.XLS"
)

activo_banca = extraer_activo_banca(archivo_activo_banca)

print("\nPRUEBA TOTAL ACTIVO - BANCA DICIEMBRE 2025")
print("Total Activo:", activo_banca)

def extraer_activo_cajas(ruta_archivo):
    """
    Extrae el total de activos de las Cajas Municipales
    desde el balance general publicado por la SBS.
    """
    datos = leer_excel_sbs(ruta_archivo)

    columna_total = None
    fila_activo = None

    # Buscar la columna del Total Cajas Municipales
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL CAJAS MUNICIPALES":
                columna_total = columna
                break

        if columna_total is not None:
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Cajas Municipales."
        )

    # Buscar la fila donde aparece TOTAL ACTIVO
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL ACTIVO":
                fila_activo = fila
                break

        if fila_activo is not None:
            break

    if fila_activo is None:
        raise ValueError(
            "No se encontró la fila correspondiente al Total Activo."
        )

    activo_total = datos.iloc[fila_activo, columna_total]

    return activo_total

archivo_activo_cajas = (
    RUTA_DATOS_CRUDOS / "C-1101-di2025.XLS"
)

activo_cajas = extraer_activo_cajas(archivo_activo_cajas)

print("\nPRUEBA TOTAL ACTIVO - CAJAS DICIEMBRE 2025")
print("Total Activo:", activo_cajas)

def extraer_margen_neto_banca(ruta_archivo):
    """
    Extrae el Margen Financiero Neto de la Banca Múltiple
    desde el Estado de Ganancias y Pérdidas de la SBS.
    """
    try:
        datos = pd.read_excel(
            ruta_archivo,
            sheet_name=1,
            header=None,
            engine="xlrd"
        )
    except Exception:
        datos = pd.read_excel(
            ruta_archivo,
            sheet_name=1,
            header=None,
            engine="openpyxl"
        )

    columna_total = None
    fila_margen = None

    # Buscar la columna del Total Banca Múltiple
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto.rstrip("*").strip() == "TOTAL BANCA MÚLTIPLE":
                columna_total = columna
                break

        if columna_total is not None:
            break

    # Buscar la fila del Margen Financiero Neto
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "MARGEN FINANCIERO NETO":
                fila_margen = fila
                break

        if fila_margen is not None:
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Banca Múltiple."
        )

    if fila_margen is None:
        raise ValueError(
            "No se encontró el Margen Financiero Neto."
        )

    margen_neto = datos.iloc[fila_margen, columna_total]

    return margen_neto


def extraer_margen_neto_cajas(ruta_archivo):
    """
    Extrae el Margen Financiero Neto de las Cajas Municipales
    desde el Estado de Ganancias y Pérdidas de la SBS.
    """
    try:
        datos = pd.read_excel(
            ruta_archivo,
            sheet_name=1,
            header=None,
            engine="xlrd"
        )
    except Exception:
        datos = pd.read_excel(
            ruta_archivo,
            sheet_name=1,
            header=None,
            engine="openpyxl"
        )

    columna_total = None
    fila_margen = None

    # Buscar la columna del Total Cajas Municipales
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL CAJAS MUNICIPALES":
                columna_total = columna
                break

        if columna_total is not None:
            break

    # Buscar la fila del Margen Financiero Neto
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "MARGEN FINANCIERO NETO":
                fila_margen = fila
                break

        if fila_margen is not None:
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Cajas Municipales."
        )

    if fila_margen is None:
        raise ValueError(
            "No se encontró el Margen Financiero Neto."
        )

    margen_neto = datos.iloc[fila_margen, columna_total]

    return margen_neto
# ---------------------------------------------------------
# PRUEBA: CAJAS MUNICIPALES - DICIEMBRE 2025
# ---------------------------------------------------------

archivo_prueba_cajas = RUTA_DATOS_CRUDOS / "C-1301-di2025.XLS"

roa_cajas, roe_cajas, morosidad_cajas = extraer_roa_roe_cajas(archivo_prueba_cajas)

print("\nPRUEBA CAJAS MUNICIPALES - DICIEMBRE 2025")
print("ROA:", roa_cajas)
print("ROE:", roe_cajas)
print("Morosidad:", morosidad_cajas)

def extraer_eficiencia_banca(ruta_archivo):
    """
    Extrae el ratio de eficiencia operativa de la Banca Múltiple,
    medido como Gastos de Operación / Margen Financiero Total.
    """
    datos = leer_excel_sbs(ruta_archivo)

    columna_total = None
    fila_eficiencia = None

    # Buscar la columna del Total Banca Múltiple
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if "TOTAL BANCA MÚLTIPLE" in texto:
                columna_total = columna
                break

        if columna_total is not None:
            break

    # Buscar la fila del ratio de eficiencia
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if (
                "GASTOS DE OPERACIÓN" in texto
                and "MARGEN FINANCIERO TOTAL" in texto
            ):
                fila_eficiencia = fila
                break

        if fila_eficiencia is not None:
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Banca Múltiple."
        )

    if fila_eficiencia is None:
        raise ValueError(
            "No se encontró el ratio de eficiencia operativa."
        )

    eficiencia = datos.iloc[fila_eficiencia, columna_total]

    return eficiencia

def extraer_eficiencia_cajas(ruta_archivo):
    """
    Extrae el ratio de eficiencia operativa de las Cajas Municipales,
    medido como Gastos de Operación / Margen Financiero Total.
    """
    datos = leer_excel_sbs(ruta_archivo)

    columna_total = None
    fila_eficiencia = None

    # Buscar la columna del Total Cajas Municipales
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if texto == "TOTAL CM":
                columna_total = columna
                break

        if columna_total is not None:
            break

    # Buscar la fila del ratio de eficiencia operativa
    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            texto = normalizar_texto(datos.iloc[fila, columna])

            if (
                "GASTOS DE OPERACIÓN" in texto
                and "MARGEN FINANCIERO TOTAL" in texto
            ):
                fila_eficiencia = fila
                break

        if fila_eficiencia is not None:
            break

    if columna_total is None:
        raise ValueError(
            "No se encontró la columna del Total Cajas Municipales."
        )

    if fila_eficiencia is None:
        raise ValueError(
            "No se encontró el ratio de eficiencia operativa."
        )

    eficiencia = datos.iloc[
        fila_eficiencia,
        columna_total
    ]

    return eficiencia

# ---------------------------------------------------------
# FUNCIÓN PARA GENERAR LOS PERIODOS DEL ESTUDIO
# ---------------------------------------------------------

def generar_periodos(fecha_inicio, fecha_corte):
    """
    Genera los periodos mensuales comprendidos entre
    la fecha de inicio y la fecha de corte.
    """

    anio_inicio, mes_inicio = map(int, fecha_inicio.split("-"))
    anio_corte, mes_corte = map(int, fecha_corte.split("-"))

    periodos = []

    anio = anio_inicio
    mes = mes_inicio

    while (anio, mes) <= (anio_corte, mes_corte):
        periodos.append((anio, mes))

        mes += 1

        if mes > 12:
            mes = 1
            anio += 1

    return periodos

# ---------------------------------------------------------
# PRUEBA DE LOS PERIODOS DEL ESTUDIO
# ---------------------------------------------------------

periodos_estudio = generar_periodos("2015-01", "2025-12")

print("\nPRUEBA DE PERIODOS")
print("Cantidad de periodos:", len(periodos_estudio))
print("Primer periodo:", periodos_estudio[0])
print("Último periodo:", periodos_estudio[-1])

# ---------------------------------------------------------
# CONSTRUCCIÓN DE LA BASE DE ROA Y ROE
# ---------------------------------------------------------

base_rentabilidad = []

for anio, mes in periodos_estudio:

    # Obtener la abreviatura del mes utilizada por la SBS
    abreviatura_mes = MESES_SBS[mes]

    # Construir los nombres de los archivos
    archivo_banca = (
        RUTA_DATOS_CRUDOS
        / f"B-2401-{abreviatura_mes}{anio}.XLS"
    )

    archivo_cajas = (
        RUTA_DATOS_CRUDOS
        / f"C-1301-{abreviatura_mes}{anio}.XLS"
    )

    archivo_activo_banca = (
        RUTA_DATOS_CRUDOS
        / f"B-2201-{abreviatura_mes}{anio}.XLS"
    )

    archivo_activo_cajas = (
        RUTA_DATOS_CRUDOS
        / f"C-1101-{abreviatura_mes}{anio}.XLS"
    )

    # Extraer ROA y ROE de Banca Múltiple
    roa_banca, roe_banca, morosidad_banca = extraer_roa_roe_banca(archivo_banca)

    # Extraer ROA y ROE de Cajas Municipales
    roa_cajas, roe_cajas, morosidad_cajas = extraer_roa_roe_cajas(archivo_cajas)

    activo_banca = extraer_activo_banca(archivo_activo_banca)
    activo_cajas = extraer_activo_cajas(archivo_activo_cajas)

    eficiencia_banca = extraer_eficiencia_banca(archivo_banca)
    eficiencia_cajas = extraer_eficiencia_cajas(archivo_cajas)

    margen_banca = extraer_margen_neto_banca(archivo_activo_banca)
    margen_cajas = extraer_margen_neto_cajas(archivo_activo_cajas)

    # Crear la fecha del periodo
    fecha = f"{anio}-{mes:02d}"

    # Agregar observación de Banca Múltiple
    base_rentabilidad.append({
    "fecha": fecha,
    "tipo_institucion": "Banca Múltiple",
    "roa": roa_banca,
    "roe": roe_banca,
    "morosidad": morosidad_banca,
    "tamano_activo": activo_banca,
    "ratio_eficiencia_operativa": eficiencia_banca,
    "margen_financiero_neto": margen_banca

})
    # Agregar observación de Cajas Municipales
    base_rentabilidad.append({
        "fecha": fecha,
        "tipo_institucion": "Cajas Municipales",
        "roa": roa_cajas,
        "roe": roe_cajas,
        "morosidad": morosidad_cajas,
        "tamano_activo": activo_cajas,
        "ratio_eficiencia_operativa": eficiencia_cajas,
        "margen_financiero_neto": margen_cajas
    })

# Convertir la lista de observaciones en un DataFrame
base_rentabilidad = pd.DataFrame(base_rentabilidad)

base_rentabilidad["fecha"] = pd.to_datetime(
    base_rentabilidad["fecha"],
    format="%Y-%m"
)

# Guardar la base procesada
ruta_salida = (
    RUTA_DATOS_PROCESADOS
    / "base_procesada_2024200495A.csv"
)

base_rentabilidad.to_csv(
    ruta_salida,
    index=False,
    encoding="utf-8-sig"
)

print("\nBASE PROCESADA GUARDADA")
print("Archivo:", ruta_salida)
print("\nBASE DE RENTABILIDAD")
print("Número de filas:", len(base_rentabilidad))
print(base_rentabilidad.head())
print("\nÚltimas filas:")
print(base_rentabilidad.tail())

print("\nVALIDACIÓN HISTÓRICA DE TOTAL ACTIVO")

errores_banca_activo = []
errores_cajas_activo = []

for anio, mes in periodos_estudio:
    abreviatura_mes = MESES_SBS[mes]

    archivo_banca = (
        RUTA_DATOS_CRUDOS
        / f"B-2201-{abreviatura_mes}{anio}.XLS"
    )

    archivo_cajas = (
        RUTA_DATOS_CRUDOS
        / f"C-1101-{abreviatura_mes}{anio}.XLS"
    )

    try:
        extraer_activo_banca(archivo_banca)
    except Exception as error:
        errores_banca_activo.append(
            (anio, mes, str(error))
        )

    try:
        extraer_activo_cajas(archivo_cajas)
    except Exception as error:
        errores_cajas_activo.append(
            (anio, mes, str(error))
        )

print("Periodos evaluados:", len(periodos_estudio))

print("\nBANCA MÚLTIPLE")
print("Errores:", len(errores_banca_activo))
print("Primeros 10 errores:")
for error in errores_banca_activo[:10]:
    print(error)

print("\nCAJAS MUNICIPALES")
print("Errores:", len(errores_cajas_activo))
print("Primeros 10 errores:")
for error in errores_cajas_activo[:10]:
    print(error)

archivo_banca_2015 = (
    RUTA_DATOS_CRUDOS / "B-2201-en2015.XLS"
)

datos_banca_2015 = leer_excel_sbs(archivo_banca_2015)

print("\nESTRUCTURA BANCA - ENERO 2015")

for fila in range(datos_banca_2015.shape[0]):
    for columna in range(datos_banca_2015.shape[1]):
        texto = normalizar_texto(
            datos_banca_2015.iloc[fila, columna]
        )

        if (
            texto == "TOTAL ACTIVO"
            or "TOTAL BANCA MÚLTIPLE" in texto
        ):
            print(
                "Fila:", fila,
                "| Columna:", columna,
                "| Texto:", texto
            )

# ---------------------------------------------------------
# VALIDACIÓN HISTÓRICA DE TOTAL ACTIVO
# ---------------------------------------------------------

errores_banca_activo = []
errores_cajas_activo = []

for anio, mes in periodos_estudio:
    abreviatura_mes = MESES_SBS[mes]

    archivo_banca = (
        RUTA_DATOS_CRUDOS
        / f"B-2201-{abreviatura_mes}{anio}.XLS"
    )

    archivo_cajas = (
        RUTA_DATOS_CRUDOS
        / f"C-1101-{abreviatura_mes}{anio}.XLS"
    )

    try:
        extraer_activo_banca(archivo_banca)
    except Exception as error:
        errores_banca_activo.append((anio, mes, str(error)))

    try:
        extraer_activo_cajas(archivo_cajas)
    except Exception as error:
        errores_cajas_activo.append((anio, mes, str(error)))

print("\nVALIDACIÓN HISTÓRICA DE TOTAL ACTIVO")
print("Banca Múltiple - Errores:", len(errores_banca_activo))
print("Cajas Municipales - Errores:", len(errores_cajas_activo))

if errores_banca_activo:
    print("\nErrores de Banca:")
    for error in errores_banca_activo[:10]:
        print(error)

if errores_cajas_activo:
    print("\nErrores de Cajas:")
    for error in errores_cajas_activo[:10]:
        print(error)

        # ---------------------------------------------------------
# REVISIÓN ESPECIAL - BANCA MARZO 2015
# ---------------------------------------------------------

archivo_banca_marzo_2015 = (
    RUTA_DATOS_CRUDOS / "B-2201-ma2015.XLS"
)

datos_banca_marzo_2015 = leer_excel_sbs(
    archivo_banca_marzo_2015
)

print("\nREVISIÓN BANCA - MARZO 2015")

for fila in range(datos_banca_marzo_2015.shape[0]):
    for columna in range(datos_banca_marzo_2015.shape[1]):
        texto = normalizar_texto(
            datos_banca_marzo_2015.iloc[fila, columna]
        )

        if "BANCA" in texto or "BANCOS" in texto:
            print(
                "Fila:", fila,
                "| Columna:", columna,
                "| Texto:", texto
            )

# ---------------------------------------------------------
# BÚSQUEDA DE MARGEN FINANCIERO NETO
# ---------------------------------------------------------

archivo_indicadores_banca = (
    RUTA_DATOS_CRUDOS / "B-2401-di2025.XLS"
)

archivo_indicadores_cajas = (
    RUTA_DATOS_CRUDOS / "C-1301-di2025.XLS"
)

datos_margen_banca = leer_excel_sbs(
    archivo_indicadores_banca
)

datos_margen_cajas = leer_excel_sbs(
    archivo_indicadores_cajas
)

print("\nPOSIBLES INDICADORES DE MARGEN - BANCA")

for fila in range(datos_margen_banca.shape[0]):
    for columna in range(datos_margen_banca.shape[1]):
        texto = normalizar_texto(
            datos_margen_banca.iloc[fila, columna]
        )

        if "MARGEN" in texto:
            print(
                "Fila:", fila,
                "| Columna:", columna,
                "| Texto:", texto
            )


print("\nPOSIBLES INDICADORES DE MARGEN - CAJAS")

for fila in range(datos_margen_cajas.shape[0]):
    for columna in range(datos_margen_cajas.shape[1]):
        texto = normalizar_texto(
            datos_margen_cajas.iloc[fila, columna]
        )

        if "MARGEN" in texto:
            print(
                "Fila:", fila,
                "| Columna:", columna,
                "| Texto:", texto
            )

# ---------------------------------------------------------
# BÚSQUEDA DE MARGEN FINANCIERO EN ESTADOS FINANCIEROS
# ---------------------------------------------------------

archivo_estado_banca = (
    RUTA_DATOS_CRUDOS / "B-2201-di2025.XLS"
)

archivo_estado_cajas = (
    RUTA_DATOS_CRUDOS / "C-1101-di2025.XLS"
)

datos_estado_banca = leer_excel_sbs(archivo_estado_banca)
datos_estado_cajas = leer_excel_sbs(archivo_estado_cajas)

print("\nMARGEN FINANCIERO EN B-2201")

for fila in range(datos_estado_banca.shape[0]):
    for columna in range(datos_estado_banca.shape[1]):
        texto = normalizar_texto(
            datos_estado_banca.iloc[fila, columna]
        )

        if "MARGEN FINANCIERO" in texto:
            print(
                "Fila:", fila,
                "| Columna:", columna,
                "| Texto:", texto
            )

print("\nMARGEN FINANCIERO EN C-1101")

for fila in range(datos_estado_cajas.shape[0]):
    for columna in range(datos_estado_cajas.shape[1]):
        texto = normalizar_texto(
            datos_estado_cajas.iloc[fila, columna]
        )

        if "MARGEN FINANCIERO" in texto:
            print(
                "Fila:", fila,
                "| Columna:", columna,
                "| Texto:", texto
            )

            print("\nBÚSQUEDA GENERAL DE MARGEN FINANCIERO - DICIEMBRE 2025")

archivos_revision = [
    "B-2201-di2025.XLS",
    "B-2401-di2025.XLS",
    "B-2315-di2025.XLS",
    "C-1101-di2025.XLS",
    "C-1301-di2025.XLS",
    "C-1207-di2025.XLS"
]

for nombre_archivo in archivos_revision:

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo
    datos_revision = leer_excel_sbs(ruta_archivo)

    print(f"\nArchivo: {nombre_archivo}")

    encontrado = False

    for fila in range(datos_revision.shape[0]):
        for columna in range(datos_revision.shape[1]):

            texto = normalizar_texto(
                datos_revision.iloc[fila, columna]
            )

            if "MARGEN" in texto:
                print(
                    "Fila:", fila,
                    "| Columna:", columna,
                    "| Texto:", texto
                )
                encontrado = True

    if not encontrado:
        print("No se encontraron indicadores con la palabra MARGEN.")


eficiencia_banca = extraer_eficiencia_banca(
    RUTA_DATOS_CRUDOS / "B-2401-di2025.XLS"
)

eficiencia_cajas = extraer_eficiencia_cajas(
    RUTA_DATOS_CRUDOS / "C-1301-di2025.XLS"
)

print("\nPRUEBA RATIO DE EFICIENCIA - DICIEMBRE 2025")
print("Banca Múltiple:", eficiencia_banca)
print("Cajas Municipales:", eficiencia_cajas)

# ---------------------------------------------------------
# VALIDACIÓN HISTÓRICA DEL RATIO DE EFICIENCIA
# ---------------------------------------------------------

errores_eficiencia_banca = []
errores_eficiencia_cajas = []

for anio, mes in periodos_estudio:
    abreviatura_mes = MESES_SBS[mes]

    archivo_banca = (
        RUTA_DATOS_CRUDOS
        / f"B-2401-{abreviatura_mes}{anio}.XLS"
    )

    archivo_cajas = (
        RUTA_DATOS_CRUDOS
        / f"C-1301-{abreviatura_mes}{anio}.XLS"
    )

    try:
        extraer_eficiencia_banca(archivo_banca)
    except Exception as error:
        errores_eficiencia_banca.append(
            (anio, mes, str(error))
        )

    try:
        extraer_eficiencia_cajas(archivo_cajas)
    except Exception as error:
        errores_eficiencia_cajas.append(
            (anio, mes, str(error))
        )

print("\nVALIDACIÓN HISTÓRICA DEL RATIO DE EFICIENCIA")
print("Periodos evaluados:", len(periodos_estudio))

print("\nBANCA MÚLTIPLE")
print("Errores:", len(errores_eficiencia_banca))

if errores_eficiencia_banca:
    print("Primeros 10 errores:")
    for error in errores_eficiencia_banca[:10]:
        print(error)

print("\nCAJAS MUNICIPALES")
print("Errores:", len(errores_eficiencia_cajas))

if errores_eficiencia_cajas:
    print("Primeros 10 errores:")
    for error in errores_eficiencia_cajas[:10]:
        print(error)


        print("\nBÚSQUEDA DE PROVISIONES - DICIEMBRE 2025")

archivos_revision = [
    "B-2201-di2025.XLS",
    "C-1101-di2025.XLS"
]

for nombre_archivo in archivos_revision:

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo
    datos_revision = leer_excel_sbs(ruta_archivo)

    print(f"\nArchivo: {nombre_archivo}")

    encontrado = False

    for fila in range(datos_revision.shape[0]):
        for columna in range(datos_revision.shape[1]):

            texto = normalizar_texto(
                datos_revision.iloc[fila, columna]
            )

            if "PROVISION" in texto:
                print(
                    "Fila:", fila,
                    "| Columna:", columna,
                    "| Texto:", texto
                )
                encontrado = True

    if not encontrado:
        print("No se encontraron conceptos con PROVISION.")

        print("\nBÚSQUEDA DE COMPONENTES DEL MARGEN - DICIEMBRE 2025")

archivos_revision = [
    "B-2401-di2025.XLS",
    "C-1301-di2025.XLS"
]

palabras_busqueda = [
    "MARGEN",
    "INGRESOS FINANCIEROS",
    "GASTOS FINANCIEROS",
    "PROVISION"
]

for nombre_archivo in archivos_revision:

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo
    datos_revision = leer_excel_sbs(ruta_archivo)

    print(f"\nArchivo: {nombre_archivo}")

    for fila in range(datos_revision.shape[0]):
        for columna in range(datos_revision.shape[1]):

            texto = normalizar_texto(
                datos_revision.iloc[fila, columna]
            )

            if any(
                palabra in texto
                for palabra in palabras_busqueda
            ):
                print(
                    "Fila:", fila,
                    "| Columna:", columna,
                    "| Texto:", texto
                )

                print("\nINSPECCIÓN DEL ESTADO DE RESULTADOS - DICIEMBRE 2025")

archivos_revision = [
    "B-2201-di2025.XLS",
    "C-1101-di2025.XLS"
]

conceptos_busqueda = [
    "MARGEN FINANCIERO",
    "INGRESOS FINANCIEROS",
    "GASTOS FINANCIEROS"
]

for nombre_archivo in archivos_revision:

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo
    datos_revision = leer_excel_sbs(ruta_archivo)

    print(f"\nArchivo: {nombre_archivo}")

    encontrado = False

    for fila in range(datos_revision.shape[0]):
        for columna in range(datos_revision.shape[1]):

            texto = normalizar_texto(
                datos_revision.iloc[fila, columna]
            )

            if any(
                concepto in texto
                for concepto in conceptos_busqueda
            ):
                print(
                    "Fila:", fila,
                    "| Columna:", columna,
                    "| Texto:", texto
                )
                encontrado = True

    if not encontrado:
        print("No se encontraron los conceptos buscados.")

        print("\nHOJAS DE LOS ESTADOS FINANCIEROS - DICIEMBRE 2025")

archivos_revision = [
    "B-2201-di2025.XLS",
    "C-1101-di2025.XLS"
]

for nombre_archivo in archivos_revision:

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo

    print(f"\nArchivo: {nombre_archivo}")

    try:
        excel = pd.ExcelFile(
            ruta_archivo,
            engine="xlrd"
        )
    except Exception:
        excel = pd.ExcelFile(
            ruta_archivo,
            engine="openpyxl"
        )

    print("Hojas encontradas:")

    for numero, hoja in enumerate(excel.sheet_names):
        print(numero, "-", hoja)

        print("\nINSPECCIÓN DE LA SEGUNDA HOJA - DICIEMBRE 2025")

archivos_revision = [
    "B-2201-di2025.XLS",
    "C-1101-di2025.XLS"
]

conceptos_busqueda = [
    "MARGEN",
    "INGRESOS FINANCIEROS",
    "GASTOS FINANCIEROS",
    "PROVISION"
]

for nombre_archivo in archivos_revision:

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo

    print(f"\nArchivo: {nombre_archivo}")

    try:
        datos = pd.read_excel(
            ruta_archivo,
            sheet_name=1,
            header=None,
            engine="xlrd"
        )
    except Exception:
        datos = pd.read_excel(
            ruta_archivo,
            sheet_name=1,
            header=None,
            engine="openpyxl"
        )

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):

            texto = normalizar_texto(
                datos.iloc[fila, columna]
            )

            if any(
                concepto in texto
                for concepto in conceptos_busqueda
            ):
                print(
                    "Fila:", fila,
                    "| Columna:", columna,
                    "| Texto:", texto
                )

                margen_banca = extraer_margen_neto_banca(
    RUTA_DATOS_CRUDOS / "B-2201-di2025.XLS"
)

margen_cajas = extraer_margen_neto_cajas(
    RUTA_DATOS_CRUDOS / "C-1101-di2025.XLS"
)


print("\nPRUEBA MARGEN FINANCIERO NETO - DICIEMBRE 2025")
print("Banca Múltiple:", margen_banca)
print("Cajas Municipales:", margen_cajas)

# ---------------------------------------------------------
# VALIDACIÓN HISTÓRICA DEL MARGEN FINANCIERO NETO
# ---------------------------------------------------------

errores_margen_banca = []
errores_margen_cajas = []

for anio, mes in periodos_estudio:
    abreviatura_mes = MESES_SBS[mes]

    archivo_banca = (
        RUTA_DATOS_CRUDOS
        / f"B-2201-{abreviatura_mes}{anio}.XLS"
    )

    archivo_cajas = (
        RUTA_DATOS_CRUDOS
        / f"C-1101-{abreviatura_mes}{anio}.XLS"
    )

    try:
        extraer_margen_neto_banca(archivo_banca)
    except Exception as error:
        errores_margen_banca.append(
            (anio, mes, str(error))
        )

    try:
        extraer_margen_neto_cajas(archivo_cajas)
    except Exception as error:
        errores_margen_cajas.append(
            (anio, mes, str(error))
        )

print("\nVALIDACIÓN HISTÓRICA DEL MARGEN FINANCIERO NETO")
print("Periodos evaluados:", len(periodos_estudio))

print("\nBANCA MÚLTIPLE")
print("Errores:", len(errores_margen_banca))

if errores_margen_banca:
    print("Primeros 10 errores:")
    for error in errores_margen_banca[:10]:
        print(error)

print("\nCAJAS MUNICIPALES")
print("Errores:", len(errores_margen_cajas))

if errores_margen_cajas:
    print("Primeros 10 errores:")
    for error in errores_margen_cajas[:10]:
        print(error)

# ---------------------------------------------------------
# VALIDACIÓN FINAL DE LA BASE PROCESADA
# ---------------------------------------------------------

print("\nVALIDACIÓN FINAL DE LA BASE")

print("\nDimensiones:")
print("Filas:", base_rentabilidad.shape[0])
print("Columnas:", base_rentabilidad.shape[1])

print("\nTipos de datos:")
print(base_rentabilidad.dtypes)

print("\nValores nulos por columna:")
print(base_rentabilidad.isnull().sum())

print("\nFilas duplicadas:")
print(base_rentabilidad.duplicated().sum())

print("\nDuplicados por fecha y tipo de institución:")
duplicados_clave = base_rentabilidad.duplicated(
    subset=["fecha", "tipo_institucion"]
).sum()
print(duplicados_clave)

print("\nObservaciones por tipo de institución:")
print(
    base_rentabilidad[
        "tipo_institucion"
    ].value_counts()
)

print("\nCantidad de fechas únicas:")
print(base_rentabilidad["fecha"].nunique())

print("\nValores mínimos de las variables:")
print(
    base_rentabilidad[
        [
            "roa",
            "roe",
            "morosidad",
            "tamano_activo",
            "ratio_eficiencia_operativa",
            "margen_financiero_neto"
        ]
    ].min()
)

print("\nValores máximos de las variables:")
print(
    base_rentabilidad[
        [
            "roa",
            "roe",
            "morosidad",
            "tamano_activo",
            "ratio_eficiencia_operativa",
            "margen_financiero_neto"
        ]
    ].max()
)