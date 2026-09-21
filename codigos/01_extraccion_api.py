# Autora: Colonio Yaringaño Lucía Pamela
# Código de matrícula: 2024200495A
# Tema: Rentabilidad de las cajas municipales frente a la banca múltiple, 2015 a 2025
# Fecha de extracción: 2026-09-20
# Propósito: Extracción automatizada y almacenamiento mediante rutas relativas

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# PARÁMETROS DEL PERÍODO DE ESTUDIO
# ---------------------------------------------------------

FECHA_INICIO = "2015-01"
FECHA_CORTE = "2025-12"
# ---------------------------------------------------------
# RUTAS DEL PROYECTO
# ---------------------------------------------------------

# Carpeta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Carpeta donde se guardarán los archivos originales de la SBS
RUTA_DATOS_CRUDOS = RUTA_PROYECTO / "datos_crudos"

# Crear la carpeta si no existe
RUTA_DATOS_CRUDOS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# ARCHIVOS OFICIALES DE LA SBS
# ---------------------------------------------------------

ARCHIVOS_SBS = {
    "banca_multiple": {
        "balance": "B-2201",
        "indicadores": "B-2401",
        "creditos_directos": "B-2315"
    },

    "cajas_municipales": {
        "balance": "C-1101",
        "indicadores": "C-1301",
        "creditos_directos": "C-1207"
    }
}
# ---------------------------------------------------------
# MESES UTILIZADOS EN LAS URL Y ARCHIVOS DE LA SBS
# ---------------------------------------------------------

MESES_SBS = {
    1: ("Enero", "en"),
    2: ("Febrero", "fe"),
    3: ("Marzo", "ma"),
    4: ("Abril", "ab"),
    5: ("Mayo", "my"),
    6: ("Junio", "jn"),
    7: ("Julio", "jl"),
    8: ("Agosto", "ag"),
    9: ("Setiembre", "se"),
    10: ("Octubre", "oc"),
    11: ("Noviembre", "no"),
    12: ("Diciembre", "di")
}
# ---------------------------------------------------------
# GENERACIÓN DEL PERÍODO DE EXTRACCIÓN
# ---------------------------------------------------------

def generar_periodos(fecha_inicio, fecha_corte):
    """
    Genera los pares (año, mes) comprendidos entre
    FECHA_INICIO y FECHA_CORTE.
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


PERIODOS = generar_periodos(FECHA_INICIO, FECHA_CORTE)
# ---------------------------------------------------------
# CONSTRUCCIÓN DE URL Y NOMBRE DE ARCHIVO SBS
# ---------------------------------------------------------

URL_BASE_SBS = "https://intranet2.sbs.gob.pe/estadistica/financiera"


def construir_url_sbs(anio, mes, codigo):
    """
    Construye la URL oficial y el nombre del archivo SBS
    correspondiente a un año, mes y código de reporte.
    """

    nombre_mes, abreviatura_mes = MESES_SBS[mes]

    nombre_archivo = (
        f"{codigo}-{abreviatura_mes}{anio}.XLS"
    )

    url = (
        f"{URL_BASE_SBS}/"
        f"{anio}/"
        f"{nombre_mes}/"
        f"{nombre_archivo}"
    )

    return url, nombre_archivo
# ------------------------------------------------------------
# GENERACIÓN DE PERÍODOS MENSUALES
# ------------------------------------------------------------

def generar_periodos(fecha_inicio, fecha_corte):
    """
    Genera todos los períodos mensuales comprendidos entre
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
# REGISTRO DE EJECUCIÓN
# ---------------------------------------------------------

RUTA_LOG = RUTA_PROYECTO / "log_ejecucion.txt"


def registrar_log(mensaje):
    """
    Registra en un archivo de texto los eventos ocurridos
    durante la ejecución del proceso de extracción.
    """

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha_hora}] {mensaje}\n")


# ---------------------------------------------------------
# FUNCIÓN DE DESCARGA DE ARCHIVOS SBS
# ---------------------------------------------------------

def descargar_archivo_sbs(url, nombre_archivo):
    """
    Descarga un archivo oficial de la SBS y lo almacena
    sin modificaciones en la carpeta datos_crudos.
    """

    ruta_destino = RUTA_DATOS_CRUDOS / nombre_archivo

    # Evita descargar nuevamente un archivo que ya existe
    if ruta_destino.exists():
        mensaje = f"Archivo ya existente: {nombre_archivo}"
        print(mensaje)
        registrar_log(mensaje)
        return "existente"

    try:
        respuesta = requests.get(url, timeout=30)

        # Verifica que el servidor responda correctamente
        if respuesta.status_code == 200:

            # Verifica que el archivo recibido tenga contenido
            if len(respuesta.content) == 0:
                mensaje = f"Error: archivo vacío - {nombre_archivo}"
                print(mensaje)
                registrar_log(mensaje)
                return "error"

            # Verifica que la respuesta corresponda a un archivo Excel
            tipo_contenido = respuesta.headers.get("Content-Type", "").lower()

            if "excel" not in tipo_contenido and "spreadsheet" not in tipo_contenido:
                mensaje = (
                    f"Error: contenido no reconocido como Excel - "
                    f"{nombre_archivo} - {tipo_contenido}"
                )
                print(mensaje)
                registrar_log(mensaje)
                return "error"

            with open(ruta_destino, "wb") as archivo:
                archivo.write(respuesta.content)

            mensaje = f"Descarga correcta: {nombre_archivo}"
            print(mensaje)
            registrar_log(mensaje)

            return "descargado"

        else:
            mensaje = (
                f"Error HTTP {respuesta.status_code}: "
                f"{nombre_archivo}"
            )

            print(mensaje)
            registrar_log(mensaje)

            return "error"

    except requests.exceptions.RequestException as error:

        mensaje = (
            f"Error de conexión: {nombre_archivo} - {error}"
        )

        print(mensaje)
        registrar_log(mensaje)

        return "error"
# ---------------------------------------------------------
# PROCESO PRINCIPAL DE EXTRACCIÓN
# ---------------------------------------------------------

# Archivos oficiales de la SBS utilizados en la investigación
ARCHIVOS_SBS = {
    "B-2201": "Banca Múltiple - Balance",
    "B-2401": "Banca Múltiple - Indicadores Financieros",
    "B-2315": "Banca Múltiple - Créditos Directos",
    "C-1101": "Cajas Municipales - Balance",
    "C-1301": "Cajas Municipales - Indicadores Financieros",
    "C-1207": "Cajas Municipales - Créditos Directos"
}


def ejecutar_extraccion(periodos):
    """
    Ejecuta la descarga programática de los archivos oficiales
    de la SBS para los períodos especificados.
    """

    total_descargados = 0
    total_existentes = 0
    total_errores = 0

    registrar_log("INICIO DEL PROCESO DE EXTRACCIÓN")

    for anio, mes in periodos:

        print(
            f"\nProcesando período: "
            f"{anio}-{mes:02d}"
        )

        for codigo, descripcion in ARCHIVOS_SBS.items():

            url, nombre_archivo = construir_url_sbs(
                anio,
                mes,
                codigo
            )

            print(f"  {descripcion}")

            resultado = descargar_archivo_sbs(
                url,
                nombre_archivo
            )

            if resultado == "descargado":
                total_descargados += 1

            elif resultado == "existente":
                total_existentes += 1

            else:
                total_errores += 1

    print("\n--------------------------------")
    print("RESUMEN DE EXTRACCIÓN")
    print("--------------------------------")
    print("Archivos descargados:", total_descargados)
    print("Archivos existentes:", total_existentes)
    print("Archivos con error:", total_errores)

    registrar_log(
        f"FIN DEL PROCESO - "
        f"Descargados: {total_descargados} - "
        f"Existentes: {total_existentes} - "
        f"Errores: {total_errores}"
    )
def validar_archivos_crudos(periodos):
    """
    Comprueba que todos los archivos oficiales esperados existan
    y que ninguno tenga un tamaño de 0 bytes.
    """

    total_esperados = 0
    total_correctos = 0
    total_faltantes = 0
    total_vacios = 0

    for anio, mes in periodos:

        for codigo in ARCHIVOS_SBS:

            # Construye el nombre que debería tener cada archivo
            _, nombre_archivo = construir_url_sbs(
                anio,
                mes,
                codigo
            )

            ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo

            total_esperados += 1

            # Comprueba si el archivo existe
            if not ruta_archivo.exists():
                print(f"FALTANTE: {nombre_archivo}")
                total_faltantes += 1
                continue

            # Comprueba si el archivo está vacío
            if ruta_archivo.stat().st_size == 0:
                print(f"VACÍO: {nombre_archivo}")
                total_vacios += 1
                continue

            total_correctos += 1

    print("\n--------------------------------")
    print("VALIDACIÓN DE DATOS CRUDOS")
    print("--------------------------------")
    print("Archivos esperados:", total_esperados)
    print("Archivos correctos:", total_correctos)
    print("Archivos faltantes:", total_faltantes)
    print("Archivos vacíos:", total_vacios)

def leer_excel_sbs(ruta_archivo):
    """
    Lee un archivo Excel de la SBS utilizando el motor
    compatible con su formato interno.
    """

    try:
        # Primero intenta leer el formato Excel antiguo (.xls)
        return pd.read_excel(
            ruta_archivo,
            sheet_name=0,
            header=None,
            engine="xlrd"
        )

    except Exception:
        # Si el archivo internamente utiliza formato moderno,
        # intenta leerlo con openpyxl
        return pd.read_excel(
            ruta_archivo,
            sheet_name=0,
            header=None,
            engine="openpyxl"
        )
    
def validar_lectura_excel(periodos):
    """
    Comprueba que todos los archivos descargados de la SBS
    puedan ser abiertos correctamente como archivos Excel.
    """

    total_evaluados = 0
    total_legibles = 0
    total_errores = 0

    for anio, mes in periodos:

        for codigo in ARCHIVOS_SBS:

            # Obtiene el nombre esperado del archivo
            _, nombre_archivo = construir_url_sbs(
                anio,
                mes,
                codigo
            )

            ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo

            total_evaluados += 1

            try:
                # Intenta abrir el archivo Excel
                leer_excel_sbs(ruta_archivo)

                total_legibles += 1

            except Exception as error:
                total_errores += 1

                mensaje = (
                    f"ERROR DE LECTURA: {nombre_archivo} - "
                    f"{error}"
                )

                print(mensaje)
                registrar_log(mensaje)

    print("\n--------------------------------")
    print("VALIDACIÓN DE LECTURA DE EXCEL")
    print("--------------------------------")
    print("Archivos evaluados:", total_evaluados)
    print("Archivos legibles:", total_legibles)
    print("Archivos con error de lectura:", total_errores)

    registrar_log(
        f"VALIDACIÓN EXCEL - "
        f"Evaluados: {total_evaluados} - "
        f"Legibles: {total_legibles} - "
        f"Errores: {total_errores}"
    )

def inspeccionar_indicadores_banca(anio, mes):
    """
    Permite inspeccionar el archivo de indicadores financieros
    de Banca Múltiple para un período específico.
    """

    # Construye el nombre del archivo B-2401
    _, nombre_archivo = construir_url_sbs(
        anio,
        mes,
        "B-2401"
    )

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo

    # Lee el archivo utilizando la función adaptativa
    datos = leer_excel_sbs(ruta_archivo)

    print("\n--------------------------------")
    print("INSPECCIÓN: INDICADORES BANCA MÚLTIPLE")
    print("--------------------------------")
    print("Archivo:", nombre_archivo)
    print("Dimensiones:", datos.shape)

    # Busca la columna correspondiente al total de Banca Múltiple
    fila_entidades = datos.iloc[5]

    for columna, valor in fila_entidades.items():
        if "Total Banca Múltiple" in str(valor):
            print("\nColumna del Total Banca Múltiple:", columna)
            print("Nombre encontrado:", valor)

            print(
                "ROE:",
                datos.iloc[29, columna]
            )

            print(
                "ROA:",
                datos.iloc[30, columna]
            )

def inspeccionar_indicadores_cajas(anio, mes):
    """
    Permite inspeccionar el archivo de indicadores financieros
    de Cajas Municipales para un período específico.
    """

    # Construye el nombre del archivo C-1301
    _, nombre_archivo = construir_url_sbs(
        anio,
        mes,
        "C-1301"
    )

    ruta_archivo = RUTA_DATOS_CRUDOS / nombre_archivo

    # Lee el archivo utilizando la función adaptativa
    datos = leer_excel_sbs(ruta_archivo)

    print("\n--------------------------------")
    print("INSPECCIÓN: INDICADORES CAJAS MUNICIPALES")
    print("--------------------------------")
    print("Archivo:", nombre_archivo)
    print("Dimensiones:", datos.shape)

     # Identifica automáticamente la columna del Total de Cajas Municipales
    fila_entidades = datos.iloc[4]

    for columna, valor in fila_entidades.items():
        nombre = str(valor).replace("\n", " ").strip()

        if nombre == "TOTAL CM":
            print("\nColumna del Total Cajas Municipales:", columna)
            print("Nombre encontrado:", nombre)

            print(
                "ROE:",
                datos.iloc[27, columna]
            )

            print(
                "ROA:",
                datos.iloc[28, columna]
            )
# ---------------------------------------------------------
# EJECUCIÓN FINAL
# ---------------------------------------------------------
# Genera los períodos oficiales definidos para la investigación
periodos_oficiales = generar_periodos(
    FECHA_INICIO,
    FECHA_CORTE
)

print("Cantidad de períodos oficiales:", len(periodos_oficiales))
print("Primer período:", periodos_oficiales[0])
print("Último período:", periodos_oficiales[-1])

# Ejecuta la extracción para todo el período de estudio
ejecutar_extraccion(periodos_oficiales)

# Valida la integridad básica de los archivos descargados
validar_archivos_crudos(periodos_oficiales)

# Valida que todos los archivos puedan abrirse como Excel
validar_lectura_excel(periodos_oficiales)

# Prueba de inspección del archivo de indicadores de Banca Múltiple
inspeccionar_indicadores_banca(2025, 12)

# Prueba de inspección del archivo de indicadores de Cajas Municipales
inspeccionar_indicadores_cajas(2025, 12)