# Autora: Colonio Yaringaño Lucía Pamela
# Código de matrícula: 2024200495A
# Tema N.º 12: Rentabilidad de las cajas municipales frente a la banca múltiple, 2015 a 2025
# Fecha de extracción: 2026-09-20

# ============================================================
# 1. IMPORTACIÓN DE LIBRERÍAS
# ============================================================

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


# ============================================================
# 2. CONFIGURACIÓN DE RUTAS
# ============================================================

RUTA_PROYECTO = Path(__file__).resolve().parent.parent

RUTA_BASE = (
    RUTA_PROYECTO
    / "datos procesados"
    / "base_procesada_2024200495A.csv"
)

RUTA_SALIDAS = RUTA_PROYECTO / "salidas"
RUTA_SALIDAS.mkdir(parents=True, exist_ok=True)


# ============================================================
# 3. CARGA Y COMPROBACIÓN DE LA BASE
# ============================================================

base = pd.read_csv(
    RUTA_BASE,
    parse_dates=["fecha"]
)

print("BASE CARGADA CORRECTAMENTE")
print(f"Filas: {base.shape[0]}")
print(f"Columnas: {base.shape[1]}")
print(f"Fecha inicial: {base['fecha'].min()}")
print(f"Fecha final: {base['fecha'].max()}")
print("\nVariables:")
print(base.columns.tolist())


# ============================================================
# 4. DEFINICIÓN DE VARIABLES
# ============================================================

variables_financieras = [
    "roa",
    "roe",
    "morosidad",
    "tamano_activo",
    "ratio_eficiencia_operativa",
    "margen_financiero_neto"
]

variables_rentabilidad = [
    "roa",
    "roe"
]

variables_complementarias = [
    "morosidad",
    "tamano_activo",
    "ratio_eficiencia_operativa",
    "margen_financiero_neto"
]

tipos_institucion = [
    "Banca Múltiple",
    "Cajas Municipales"
]


# ============================================================
# 5. ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

estadisticas_descriptivas = (
    base
    .groupby("tipo_institucion")[variables_financieras]
    .agg(["count", "mean", "std", "min", "median", "max"])
    .round(4)
)

print("\nESTADÍSTICAS DESCRIPTIVAS POR TIPO DE INSTITUCIÓN")
print(estadisticas_descriptivas)

ruta_descriptivos = (
    RUTA_SALIDAS
    / "estadisticas_descriptivas.csv"
)

estadisticas_descriptivas.to_csv(
    ruta_descriptivos,
    encoding="utf-8-sig"
)

print("\nTABLA DESCRIPTIVA GUARDADA")
print(f"Archivo: {ruta_descriptivos}")


# ============================================================
# 6. RESUMEN DE ROA Y ROE
# ============================================================

print("\nRESUMEN DE RENTABILIDAD")

for tipo in tipos_institucion:

    datos_tipo = (
        base[base["tipo_institucion"] == tipo]
        .sort_values("fecha")
    )

    print(f"\n{tipo.upper()}")

    for variable in variables_rentabilidad:

        fila_min = datos_tipo.loc[
            datos_tipo[variable].idxmin()
        ]

        fila_max = datos_tipo.loc[
            datos_tipo[variable].idxmax()
        ]

        print(f"\n{variable.upper()}")
        print(
            f"Promedio: "
            f"{datos_tipo[variable].mean():.4f}%"
        )
        print(
            f"Mínimo: {fila_min[variable]:.4f}% "
            f"({fila_min['fecha'].strftime('%Y-%m')})"
        )
        print(
            f"Máximo: {fila_max[variable]:.4f}% "
            f"({fila_max['fecha'].strftime('%Y-%m')})"
        )


# ============================================================
# 7. RESUMEN DE VARIABLES COMPLEMENTARIAS
# ============================================================

print("\nRESUMEN DE VARIABLES COMPLEMENTARIAS")

for tipo in tipos_institucion:

    datos_tipo = base[
        base["tipo_institucion"] == tipo
    ]

    print(f"\n{tipo.upper()}")

    for variable in variables_complementarias:

        print(f"\n{variable.upper()}")
        print(
            f"Promedio: "
            f"{datos_tipo[variable].mean():.4f}"
        )
        print(
            f"Mínimo: "
            f"{datos_tipo[variable].min():.4f}"
        )
        print(
            f"Máximo: "
            f"{datos_tipo[variable].max():.4f}"
        )


# ============================================================
# 8. GRÁFICOS DE EVOLUCIÓN TEMPORAL
# ============================================================

titulos_variables = {
    "roa": "Evolución mensual del ROA, 2015-2025",
    "roe": "Evolución mensual del ROE, 2015-2025",
    "morosidad": "Evolución de la morosidad, 2015-2025",
    "tamano_activo": "Evolución del tamaño del activo, 2015-2025",
    "ratio_eficiencia_operativa":
        "Evolución del ratio de eficiencia operativa, 2015-2025",
    "margen_financiero_neto":
        "Evolución del margen financiero neto, 2015-2025"
}

etiquetas_eje_y = {
    "roa": "ROA (%)",
    "roe": "ROE (%)",
    "morosidad": "Morosidad (%)",
    "tamano_activo": "Tamaño del activo (S/ miles)",
    "ratio_eficiencia_operativa":
        "Ratio de eficiencia operativa (%)",
    "margen_financiero_neto":
        "Margen financiero neto (S/ miles)"
}

for variable in variables_financieras:

    plt.figure(figsize=(10, 6))

    for tipo in tipos_institucion:

        datos_tipo = (
            base[base["tipo_institucion"] == tipo]
            .sort_values("fecha")
        )

        plt.plot(
            datos_tipo["fecha"],
            datos_tipo[variable],
            label=tipo
        )

    plt.title(titulos_variables[variable])
    plt.xlabel("Fecha")
    plt.ylabel(etiquetas_eje_y[variable])
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    ruta_grafico = (
        RUTA_SALIDAS
        / f"evolucion_{variable}.png"
    )

    plt.savefig(
        ruta_grafico,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Gráfico guardado: "
        f"{ruta_grafico.name}"
    )


# ============================================================
# 9. CONSTRUCCIÓN DE DIFERENCIAS MENSUALES
# ============================================================

comparacion = base.pivot(
    index="fecha",
    columns="tipo_institucion",
    values=variables_financieras
)

tabla_diferencias = pd.DataFrame(
    index=comparacion.index
)

for variable in variables_financieras:

    tabla_diferencias[f"diferencia_{variable}"] = (
        comparacion[(variable, "Banca Múltiple")]
        - comparacion[(variable, "Cajas Municipales")]
    )

ruta_diferencias = (
    RUTA_SALIDAS
    / "diferencias_mensuales.csv"
)

tabla_diferencias.to_csv(
    ruta_diferencias,
    encoding="utf-8-sig"
)

print("\nTABLA DE DIFERENCIAS MENSUALES GUARDADA")
print(f"Archivo: {ruta_diferencias}")
print(f"Filas: {len(tabla_diferencias)}")
print(
    f"Columnas: "
    f"{len(tabla_diferencias.columns)}"
)


# ============================================================
# 10. RESUMEN DE DIFERENCIAS Y AUTOCORRELACIÓN
# ============================================================

print("\nDIFERENCIAS MENSUALES BANCA - CAJAS")

for variable in variables_financieras:

    diferencia = (
        tabla_diferencias[
            f"diferencia_{variable}"
        ]
    )

    meses_banca_mayor = (
        diferencia > 0
    ).sum()

    meses_cajas_mayor = (
        diferencia < 0
    ).sum()

    autocorrelacion = (
        diferencia.autocorr(lag=1)
    )

    print(f"\n{variable.upper()}")
    print(
        f"Diferencia promedio: "
        f"{diferencia.mean():.4f}"
    )
    print(
        f"Meses con valor mayor en Banca: "
        f"{meses_banca_mayor} "
        f"de {len(diferencia)}"
    )
    print(
        f"Meses con valor mayor en Cajas: "
        f"{meses_cajas_mayor} "
        f"de {len(diferencia)}"
    )
    print(
        f"Autocorrelación rezago 1: "
        f"{autocorrelacion:.4f}"
    )


# ============================================================
# 11. INFERENCIA HAC / NEWEY-WEST
# ============================================================

resultados_hac = []

print("\nRESULTADOS HAC / NEWEY-WEST")

for variable in tabla_diferencias.columns:

    y = tabla_diferencias[
        variable
    ].dropna()

    # La constante representa la diferencia promedio.
    X = sm.add_constant(
        pd.DataFrame(index=y.index)
    )

    modelo_hac = sm.OLS(
        y,
        X
    ).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": 12}
    )

    intervalo = (
        modelo_hac
        .conf_int()
        .loc["const"]
    )

    resultados_hac.append({
        "variable": variable,
        "diferencia_promedio":
            modelo_hac.params["const"],
        "error_estandar_hac":
            modelo_hac.bse["const"],
        "estadistico_t":
            modelo_hac.tvalues["const"],
        "valor_p":
            modelo_hac.pvalues["const"],
        "ic_95_inferior":
            intervalo.iloc[0],
        "ic_95_superior":
            intervalo.iloc[1]
    })

    print(f"\n{variable.upper()}")
    print(
        f"Diferencia promedio: "
        f"{modelo_hac.params['const']:.4f}"
    )
    print(
        f"Error estándar HAC: "
        f"{modelo_hac.bse['const']:.4f}"
    )
    print(
        f"Estadístico t: "
        f"{modelo_hac.tvalues['const']:.4f}"
    )

    valor_p = modelo_hac.pvalues["const"]

    if valor_p < 0.001:
        print("Valor p: < 0.001")
    else:
        print(f"Valor p: {valor_p:.6f}")

    print(
        f"IC 95%: "
        f"[{intervalo.iloc[0]:.4f}, "
        f"{intervalo.iloc[1]:.4f}]"
    )


tabla_hac = pd.DataFrame(
    resultados_hac
)

ruta_hac = (
    RUTA_SALIDAS
    / "resultados_hac.csv"
)

tabla_hac.to_csv(
    ruta_hac,
    index=False,
    encoding="utf-8-sig"
)

print("\nRESULTADOS HAC GUARDADOS")
print(f"Archivo: {ruta_hac}")
print(f"Filas: {len(tabla_hac)}")
print(
    f"Columnas: "
    f"{len(tabla_hac.columns)}"
)


# ============================================================
# 12. PRUEBA DE ROBUSTEZ HAC
# ============================================================

rezagos_robustez = [
    3,
    6,
    12,
    18,
    24
]

resultados_robustez = []

print("\nPRUEBA DE ROBUSTEZ HAC")

for variable in tabla_diferencias.columns:

    y = tabla_diferencias[
        variable
    ].dropna()

    X = sm.add_constant(
        pd.DataFrame(index=y.index)
    )

    print(f"\n{variable.upper()}")

    for rezago in rezagos_robustez:

        modelo_robusto = sm.OLS(
            y,
            X
        ).fit(
            cov_type="HAC",
            cov_kwds={"maxlags": rezago}
        )

        resultados_robustez.append({
            "variable": variable,
            "rezago": rezago,
            "diferencia_promedio":
                modelo_robusto.params["const"],
            "error_estandar_hac":
                modelo_robusto.bse["const"],
            "estadistico_t":
                modelo_robusto.tvalues["const"],
            "valor_p":
                modelo_robusto.pvalues["const"]
        })

        valor_p = (
            modelo_robusto
            .pvalues["const"]
        )

        if valor_p < 0.001:
            valor_p_texto = "< 0.001"
        else:
            valor_p_texto = (
                f"{valor_p:.6f}"
            )

        print(
            f"Rezago {rezago:>2}: "
            f"coef="
            f"{modelo_robusto.params['const']:.4f}, "
            f"EE="
            f"{modelo_robusto.bse['const']:.4f}, "
            f"p={valor_p_texto}"
        )


tabla_robustez = pd.DataFrame(
    resultados_robustez
)

ruta_robustez = (
    RUTA_SALIDAS
    / "robustez_hac.csv"
)

tabla_robustez.to_csv(
    ruta_robustez,
    index=False,
    encoding="utf-8-sig"
)

print("\nPRUEBA DE ROBUSTEZ HAC GUARDADA")
print(f"Archivo: {ruta_robustez}")
print(
    f"Filas: "
    f"{len(tabla_robustez)}"
)
print(
    f"Columnas: "
    f"{len(tabla_robustez.columns)}"
)


# ============================================================
# 13. CORRELACIONES ENTRE VARIABLES FINANCIERAS
# ============================================================

print("\nCORRELACIONES ENTRE VARIABLES FINANCIERAS")

for tipo in tipos_institucion:

    datos_tipo = base[
        base["tipo_institucion"] == tipo
    ]

    matriz_correlacion = (
        datos_tipo[
            variables_financieras
        ]
        .corr()
        .round(4)
    )

    print(f"\n{tipo.upper()}")

    # Se muestran las correlaciones de ROA y ROE
    # con las variables financieras complementarias.
    for rentabilidad in variables_rentabilidad:

        print(f"\n{rentabilidad.upper()}")

        for variable in variables_complementarias:

            correlacion = (
                matriz_correlacion.loc[
                    rentabilidad,
                    variable
                ]
            )

            print(
                f"{variable}: "
                f"{correlacion:.4f}"
            )

    if tipo == "Banca Múltiple":
        nombre_archivo = (
            "correlaciones_banca.csv"
        )
    else:
        nombre_archivo = (
            "correlaciones_cajas.csv"
        )

    matriz_correlacion.to_csv(
        RUTA_SALIDAS / nombre_archivo,
        encoding="utf-8-sig"
    )


# ============================================================
# 14. RESUMEN FINAL DE ARCHIVOS GENERADOS
# ============================================================

archivos_esperados = [
    "estadisticas_descriptivas.csv",
    "evolucion_roa.png",
    "evolucion_roe.png",
    "evolucion_morosidad.png",
    "evolucion_tamano_activo.png",
    "evolucion_ratio_eficiencia_operativa.png",
    "evolucion_margen_financiero_neto.png",
    "correlaciones_banca.csv",
    "correlaciones_cajas.csv",
    "diferencias_mensuales.csv",
    "resultados_hac.csv",
    "robustez_hac.csv"
]

archivos_faltantes = [
    archivo
    for archivo in archivos_esperados
    if not (
        RUTA_SALIDAS / archivo
    ).exists()
]

print("\n========================================")
print("VALIDACIÓN FINAL DEL ANÁLISIS")
print("========================================")

print(
    f"Archivos esperados: "
    f"{len(archivos_esperados)}"
)

print(
    f"Archivos encontrados: "
    f"{len(archivos_esperados) - len(archivos_faltantes)}"
)

print(
    f"Archivos faltantes: "
    f"{len(archivos_faltantes)}"
)

if len(archivos_faltantes) == 0:
    print("Estado: ANÁLISIS COMPLETADO CORRECTAMENTE")
else:
    print("Estado: REVISAR ARCHIVOS FALTANTES")

    for archivo in archivos_faltantes:
        print(f"- {archivo}")