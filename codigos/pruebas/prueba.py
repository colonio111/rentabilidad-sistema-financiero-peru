import requests
import pandas as pd
from pathlib import Path
# ---------------------------------------------------------
# PRUEBA DE DESCARGA SBS
# Periodo de prueba: diciembre de 2015
# ---------------------------------------------------------

# Carpeta donde guardaremos temporalmente los archivos
carpeta = Path("prueba_sbs")
carpeta.mkdir(exist_ok=True)

# Archivos que queremos comprobar
archivos = {
    "B-2201": "Banca Múltiple - Balance",
    "B-2401": "Banca Múltiple - Indicadores",
    "C-1101": "Cajas Municipales - Balance",
    "C-1301": "Cajas Municipales - Indicadores"
}

# Dirección base de la SBS
url_base = "https://intranet2.sbs.gob.pe/estadistica/financiera/2015/Diciembre/"

for codigo, descripcion in archivos.items():

    nombre_archivo = f"{codigo}-di2015.XLS"
    url = url_base + nombre_archivo

    print("\n--------------------------------")
    print(descripcion)
    print("URL:", url)

    respuesta = requests.get(url, timeout=30)

    print("Código HTTP:", respuesta.status_code)
    print("Tipo de contenido:", respuesta.headers.get("Content-Type"))
    print("Tamaño:", len(respuesta.content), "bytes")

    if respuesta.status_code == 200:

        ruta = carpeta / nombre_archivo

        with open(ruta, "wb") as archivo:
            archivo.write(respuesta.content)

        print("DESCARGA CORRECTA")
        print("Guardado en:", ruta)

    else:
        print("ERROR EN LA DESCARGA")
# ---------------------------------------------------------
# PRUEBA DE DESCARGA SBS
# Periodo de prueba: diciembre de 2015
# ---------------------------------------------------------

# Carpeta donde guardaremos temporalmente los archivos
carpeta = Path("prueba_sbs")
carpeta.mkdir(exist_ok=True)

# Archivos que queremos comprobar
archivos = {
    "B-2201": "Banca Múltiple - Balance",
    "B-2401": "Banca Múltiple - Indicadores",
    "C-1101": "Cajas Municipales - Balance",
    "C-1301": "Cajas Municipales - Indicadores"
}

# Dirección base de la SBS
url_base = "https://intranet2.sbs.gob.pe/estadistica/financiera/2015/Diciembre/"

for codigo, descripcion in archivos.items():

    nombre_archivo = f"{codigo}-di2015.XLS"
    url = url_base + nombre_archivo

    print("\n--------------------------------")
    print(descripcion)
    print("URL:", url)

    respuesta = requests.get(url, timeout=30)

    print("Código HTTP:", respuesta.status_code)
    print("Tipo de contenido:", respuesta.headers.get("Content-Type"))
    print("Tamaño:", len(respuesta.content), "bytes")

    if respuesta.status_code == 200:

        ruta = carpeta / nombre_archivo

        with open(ruta, "wb") as archivo:
            archivo.write(respuesta.content)

        print("DESCARGA CORRECTA")
        print("Guardado en:", ruta)

    else:
        print("ERROR EN LA DESCARGA")
        
# ---------------------------------------------------------
# PRUEBA 2: LECTURA DE ARCHIVO XLS DE SBS
# Archivo: B-2401 - Indicadores Financieros
# Periodo: diciembre de 2015
# ---------------------------------------------------------

ruta = Path("prueba_sbs") / "B-2401-di2015.XLS"

print("Archivo que se intentará leer:")
print(ruta)

# Comprobar que el archivo existe
if ruta.exists():
    print("\nEl archivo existe correctamente.")
else:
    print("\nERROR: No se encontró el archivo.")

# Abrir el archivo Excel y conocer sus hojas
excel = pd.ExcelFile(ruta, engine="xlrd")

print("\nHojas encontradas:")
print(excel.sheet_names)

# Leer la primera hoja sin asumir encabezados
datos = pd.read_excel(
    ruta,
    sheet_name=0,
    header=None,
    engine="xlrd"
)

print("\nDimensiones de la primera hoja:")
print("Filas:", datos.shape[0])
print("Columnas:", datos.shape[1])

print("\nPrimeras 20 filas:")
print(datos.head(20).to_string())
# ---------------------------------------------------------
# PRUEBA 3: LOCALIZACIÓN DE VARIABLES
# Archivo: B-2401 - Indicadores Financieros
# ---------------------------------------------------------

print("\n========== PRUEBA 3 ==========")

# Palabras que queremos localizar
terminos = [
    "activo promedio",
    "patrimonio promedio",
    "créditos atrasados",
    "creditos atrasados",
    "morosidad",
    "ROA",
    "ROE"
]

# Buscar cada término en todas las celdas
for termino in terminos:

    print(f"\nBUSCANDO: {termino}")

    encontrado = False

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):

            valor = datos.iat[fila, columna]

            if pd.notna(valor):
                texto = str(valor)

                if termino.lower() in texto.lower():
                    print(
                        f"Encontrado -> "
                        f"fila {fila}, columna {columna}: {texto}"
                    )
                    encontrado = True

    if not encontrado:
        print("No encontrado")
        # ---------------------------------------------------------
# PRUEBA 3B: ACTIVO TOTAL Y CRÉDITOS DIRECTOS
# Archivo: B-2201 - Balance
# ---------------------------------------------------------

print("\n========== PRUEBA 3B ==========")

ruta_balance = Path("prueba_sbs") / "B-2201-di2015.XLS"

balance = pd.read_excel(
    ruta_balance,
    sheet_name=0,
    header=None,
    engine="xlrd"
)

terminos_balance = [
    "TOTAL ACTIVO",
    "CRÉDITOS DIRECTOS",
    "CREDITOS DIRECTOS"
]

for termino in terminos_balance:

    print(f"\nBUSCANDO: {termino}")
    encontrado = False

    for fila in range(balance.shape[0]):
        for columna in range(balance.shape[1]):

            valor = balance.iat[fila, columna]

            if pd.notna(valor):
                texto = str(valor)

                if termino.lower() in texto.lower():
                    print(
                        f"Encontrado -> "
                        f"fila {fila}, columna {columna}: {texto}"
                    )
                    encontrado = True

    if not encontrado:
        print("No encontrado")
        # ---------------------------------------------------------
# PRUEBA 3C: IDENTIFICAR EL NOMBRE DE LOS CRÉDITOS
# ---------------------------------------------------------

print("\n========== PRUEBA 3C ==========")

terminos_creditos = [
    "crédito",
    "credito",
    "colocaciones"
]

for termino in terminos_creditos:

    print(f"\nBUSCANDO: {termino}")
    encontrado = False

    for fila in range(balance.shape[0]):
        for columna in range(balance.shape[1]):

            valor = balance.iat[fila, columna]

            if pd.notna(valor):
                texto = str(valor)

                if termino.lower() in texto.lower():
                    print(
                        f"Encontrado -> "
                        f"fila {fila}, columna {columna}: {texto}"
                    )
                    encontrado = True

    if not encontrado:
        print("No encontrado")
        print("\n========== CONTEXTO DEL BALANCE ==========")

print(
    balance.iloc[20:61, 0:12].to_string(
        index=True,
        header=True
    )
)
# ---------------------------------------------------------
# PRUEBA 3D: DESCARGA DE CRÉDITOS DIRECTOS
# Diciembre 2015
# ---------------------------------------------------------

print("\n========== PRUEBA 3D ==========")

archivos_creditos = {
    "B-2315-di2015.XLS": "Banca Múltiple",
    "C-1207-di2015.XLS": "Cajas Municipales"
}

url_base = (
    "https://intranet2.sbs.gob.pe/"
    "estadistica/financiera/2015/Diciembre/"
)

for nombre_archivo, institucion in archivos_creditos.items():

    url = url_base + nombre_archivo

    print("\n--------------------------------")
    print(institucion)
    print("Archivo:", nombre_archivo)
    print("URL:", url)

    respuesta = requests.get(url, timeout=30)

    print("Código HTTP:", respuesta.status_code)
    print(
        "Tipo de contenido:",
        respuesta.headers.get("Content-Type")
    )
    print("Tamaño:", len(respuesta.content), "bytes")

    if respuesta.status_code == 200:

        ruta_salida = Path("prueba_sbs") / nombre_archivo

        with open(ruta_salida, "wb") as archivo:
            archivo.write(respuesta.content)

        print("DESCARGA CORRECTA")
        print("Guardado en:", ruta_salida)

    else:
        print("ERROR EN LA DESCARGA")
        # ---------------------------------------------------------
# PRUEBA 3E: LEER CUADROS DE CRÉDITOS DIRECTOS
# ---------------------------------------------------------

print("\n========== PRUEBA 3E ==========")

archivos_creditos = {
    "Banca Múltiple": "B-2315-di2015.XLS",
    "Cajas Municipales": "C-1207-di2015.XLS"
}

for institucion, nombre_archivo in archivos_creditos.items():

    print("\n========================================")
    print(institucion)
    print("Archivo:", nombre_archivo)
    print("========================================")

    ruta = Path("prueba_sbs") / nombre_archivo

    datos_creditos = pd.read_excel(
        ruta,
        sheet_name=0,
        header=None,
        engine="xlrd"
    )

    print(
        "Dimensiones:",
        datos_creditos.shape[0],
        "filas x",
        datos_creditos.shape[1],
        "columnas"
    )

    print("\nContenido del archivo:")

    print(
        datos_creditos.to_string(
            index=True,
            header=True
        )
    )
# ---------------------------------------------------------
# PRUEBA 3F: UBICAR FILAS Y COLUMNAS DEL TOTAL
# ---------------------------------------------------------

print("\n========== PRUEBA 3F ==========")

archivos = {
    "Banca Múltiple": "B-2315-di2015.XLS",
    "Cajas Municipales": "C-1207-di2015.XLS"
}

for institucion, nombre_archivo in archivos.items():

    print("\n----------------------------------------")
    print(institucion)
    print("----------------------------------------")

    ruta = Path("prueba_sbs") / nombre_archivo

    df = pd.read_excel(
        ruta,
        sheet_name=0,
        header=None,
        engine="xlrd"
    )

    # Buscar celdas que contengan la palabra TOTAL
    for fila in range(df.shape[0]):
        for columna in range(df.shape[1]):

            valor = df.iat[fila, columna]

            if pd.notna(valor):

                texto = str(valor)

                if "TOTAL" in texto.upper():

                    print(
                        f"Fila {fila}, columna {columna}: "
                        f"{texto}"
                    )

                    # Mostrar toda esa fila
                    print("Contenido completo de la fila:")

                    for c in range(df.shape[1]):

                        print(
                            f"  columna {c}: "
                            f"{df.iat[fila, c]}"
                        )
# ---------------------------------------------------------
# PRUEBA 4A: CONSISTENCIA TEMPORAL
# Descarga de archivos de diciembre de 2025
# ---------------------------------------------------------

print("\n========== PRUEBA 4A ==========")

carpeta_2025 = Path("prueba_sbs_2025")
carpeta_2025.mkdir(exist_ok=True)

archivos_2025 = {
    "B-2201-di2025.XLS": "Banca Múltiple - Balance",
    "B-2401-di2025.XLS": "Banca Múltiple - Indicadores",
    "B-2315-di2025.XLS": "Banca Múltiple - Créditos Directos",

    "C-1101-di2025.XLS": "Cajas Municipales - Balance",
    "C-1301-di2025.XLS": "Cajas Municipales - Indicadores",
    "C-1207-di2025.XLS": "Cajas Municipales - Créditos Directos"
}

url_base_2025 = (
    "https://intranet2.sbs.gob.pe/"
    "estadistica/financiera/2025/Diciembre/"
)

for nombre_archivo, descripcion in archivos_2025.items():

    url = url_base_2025 + nombre_archivo

    print("\n--------------------------------")
    print(descripcion)
    print("Archivo:", nombre_archivo)
    print("URL:", url)

    try:

        respuesta = requests.get(
            url,
            timeout=30
        )

        print(
            "Código HTTP:",
            respuesta.status_code
        )

        print(
            "Tipo de contenido:",
            respuesta.headers.get("Content-Type")
        )

        print(
            "Tamaño:",
            len(respuesta.content),
            "bytes"
        )

        if respuesta.status_code == 200:

            ruta_salida = (
                carpeta_2025 /
                nombre_archivo
            )

            with open(
                ruta_salida,
                "wb"
            ) as archivo:

                archivo.write(
                    respuesta.content
                )

            print("DESCARGA CORRECTA")
            print(
                "Guardado en:",
                ruta_salida
            )

        else:

            print(
                "ARCHIVO NO DISPONIBLE"
            )

    except requests.RequestException as error:

        print(
            "ERROR DE CONEXIÓN:",
            error
        )
        # ---------------------------------------------------------
# PRUEBA 4B: VERIFICAR VARIABLES EN DICIEMBRE DE 2025
# ---------------------------------------------------------

print("\n========== PRUEBA 4B ==========")

pruebas_2025 = {
    "B-2401-di2025.XLS": [
        "Utilidad Neta Anualizada / Patrimonio Promedio",
        "Utilidad Neta Anualizada / Activo Promedio",
        "Créditos Atrasados (criterio SBS)"
    ],

    "C-1301-di2025.XLS": [
        "Utilidad Neta Anualizada / Patrimonio Promedio",
        "Utilidad Neta Anualizada / Activo Promedio",
        "Créditos Atrasados (criterio SBS)"
    ],

    "B-2201-di2025.XLS": [
        "TOTAL ACTIVO"
    ],

    "C-1101-di2025.XLS": [
        "TOTAL ACTIVO"
    ],

    "B-2315-di2025.XLS": [
        "TOTAL BANCA MÚLTIPLE",
        "Total Créditos"
    ],

    "C-1207-di2025.XLS": [
        "TOTAL CAJAS MUNICIPALES",
        "Total Créditos"
    ]
}

for nombre_archivo, terminos in pruebas_2025.items():

    print("\n========================================")
    print("ARCHIVO:", nombre_archivo)
    print("========================================")

    ruta = Path("prueba_sbs_2025") / nombre_archivo

    df = pd.read_excel(
        ruta,
        sheet_name=0,
        header=None,
        engine="xlrd"
    )

    print(
        "Dimensiones:",
        df.shape[0],
        "filas x",
        df.shape[1],
        "columnas"
    )

    for termino in terminos:

        print(f"\nBUSCANDO: {termino}")

        coincidencias = []

        for fila in range(df.shape[0]):
            for columna in range(df.shape[1]):

                valor = df.iat[fila, columna]

                if pd.notna(valor):

                    texto = str(valor)

                    if termino.lower() in texto.lower():

                        coincidencias.append(
                            (fila, columna, texto)
                        )

        if coincidencias:

            for fila, columna, texto in coincidencias:

                print(
                    f"Encontrado -> "
                    f"fila {fila}, "
                    f"columna {columna}: "
                    f"{texto}"
                )

        else:

            print("NO ENCONTRADO")

# ---------------------------------------------------------
# FUNCIÓN PARA LEER ARCHIVOS EXCEL DE LA SBS
# Detecta automáticamente XLS antiguo o XLSX moderno
# ---------------------------------------------------------

def leer_excel_sbs(ruta):

    try:
        # Primero intenta leer como Excel antiguo (.xls)
        return pd.read_excel(
            ruta,
            sheet_name=0,
            header=None,
            engine="xlrd"
        )

    except Exception:

        # Si falla, intenta como Excel moderno (.xlsx)
        return pd.read_excel(
            ruta,
            sheet_name=0,
            header=None,
            engine="openpyxl"
        )