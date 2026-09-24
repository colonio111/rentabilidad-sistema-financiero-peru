# Autora: Colonio Yaringaño Lucía Pamela
# Código de matrícula: 2024200495A
# Tema N.º 12: Rentabilidad de las cajas municipales frente a la banca múltiple, 2015 a 2025
# Fecha de extracción: 2026-09-20
# ============================================================
# IMPORTACIÓN DE LIBRERÍAS
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


# ============================================================
# CONFIGURACIÓN DE RUTAS
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
# CARGA DE LA BASE PROCESADA
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
# ESTADÍSTICA DESCRIPTIVA POR TIPO DE INSTITUCIÓN
# ============================================================

variables_financieras = [
    "roa",
    "roe",
    "morosidad",
    "tamano_activo",
    "ratio_eficiencia_operativa",
    "margen_financiero_neto"
]

estadisticas_descriptivas = (
    base
    .groupby("tipo_institucion")[variables_financieras]
    .agg(["count", "mean", "std", "min", "median", "max"])
    .round(4)
)

print("\nESTADÍSTICAS DESCRIPTIVAS POR TIPO DE INSTITUCIÓN")
print(estadisticas_descriptivas)

# ============================================================
# GUARDADO DE ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

ruta_descriptivos = RUTA_SALIDAS / "estadisticas_descriptivas.csv"

estadisticas_descriptivas.to_csv(
    ruta_descriptivos,
    encoding="utf-8-sig"
)

print("\nTABLA DESCRIPTIVA GUARDADA")
print(f"Archivo: {ruta_descriptivos}")

# ============================================================
# EVOLUCIÓN TEMPORAL DEL ROA
# ============================================================

for tipo in base["tipo_institucion"].unique():
    datos_tipo = base[base["tipo_institucion"] == tipo]

    plt.plot(
        datos_tipo["fecha"],
        datos_tipo["roa"],
        label=tipo
    )

plt.title("Evolución mensual del ROA, 2015-2025")
plt.xlabel("Fecha")
plt.ylabel("ROA (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

ruta_grafico_roa = RUTA_SALIDAS / "evolucion_roa.png"
plt.savefig(ruta_grafico_roa, dpi=300)
plt.close()

print("\nGRÁFICO DE ROA GUARDADO")
print(f"Archivo: {ruta_grafico_roa}")

# ============================================================
# EVOLUCIÓN TEMPORAL DEL ROE
# ============================================================

for tipo in base["tipo_institucion"].unique():
    datos_tipo = base[base["tipo_institucion"] == tipo]

    plt.plot(
        datos_tipo["fecha"],
        datos_tipo["roe"],
        label=tipo
    )

plt.title("Evolución mensual del ROE, 2015-2025")
plt.xlabel("Fecha")
plt.ylabel("ROE (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

ruta_grafico_roe = RUTA_SALIDAS / "evolucion_roe.png"
plt.savefig(ruta_grafico_roe, dpi=300)
plt.close()

print("\nGRÁFICO DE ROE GUARDADO")
print(f"Archivo: {ruta_grafico_roe}")

# ============================================================
# RESUMEN DE RENTABILIDAD: ROA Y ROE
# ============================================================

for tipo in base["tipo_institucion"].unique():

    datos_tipo = (
        base[base["tipo_institucion"] == tipo]
        .sort_values("fecha")
    )

    print(f"\n{tipo.upper()}")

    for variable in ["roa", "roe"]:

        fila_min = datos_tipo.loc[datos_tipo[variable].idxmin()]
        fila_max = datos_tipo.loc[datos_tipo[variable].idxmax()]

        print(f"\n{variable.upper()}")
        print(f"Promedio: {datos_tipo[variable].mean():.4f}%")
        print(
            f"Mínimo: {fila_min[variable]:.4f}% "
            f"({fila_min['fecha'].strftime('%Y-%m')})"
        )
        print(
            f"Máximo: {fila_max[variable]:.4f}% "
            f"({fila_max['fecha'].strftime('%Y-%m')})"
        )

# ============================================================
# DIFERENCIAS MENSUALES DE RENTABILIDAD
# ============================================================

comparacion = base.pivot(
    index="fecha",
    columns="tipo_institucion",
    values=["roa", "roe"]
)

comparacion["diferencia_roa"] = (
    comparacion[("roa", "Banca Múltiple")]
    - comparacion[("roa", "Cajas Municipales")]
)

comparacion["diferencia_roe"] = (
    comparacion[("roe", "Banca Múltiple")]
    - comparacion[("roe", "Cajas Municipales")]
)

print("\nDIFERENCIAS MENSUALES DE RENTABILIDAD")
print(
    f"Diferencia promedio ROA: "
    f"{comparacion['diferencia_roa'].mean():.4f} puntos porcentuales"
)

print(
    f"Diferencia promedio ROE: "
    f"{comparacion['diferencia_roe'].mean():.4f} puntos porcentuales"
)

print(
    f"Meses con ROA mayor en Banca Múltiple: "
    f"{(comparacion['diferencia_roa'] > 0).sum()} de {len(comparacion)}"
)

print(
    f"Meses con ROE mayor en Banca Múltiple: "
    f"{(comparacion['diferencia_roe'] > 0).sum()} de {len(comparacion)}"
)

# ============================================================
# AUTOCORRELACIÓN DE LAS DIFERENCIAS DE RENTABILIDAD
# ============================================================

autocorrelacion_roa = comparacion["diferencia_roa"].autocorr(lag=1)
autocorrelacion_roe = comparacion["diferencia_roe"].autocorr(lag=1)

print("\nAUTOCORRELACIÓN DE LAS DIFERENCIAS")
print(f"ROA - autocorrelación rezago 1: {autocorrelacion_roa:.4f}")
print(f"ROE - autocorrelación rezago 1: {autocorrelacion_roe:.4f}")

# ============================================================
# INFERENCIA CON ERRORES ESTÁNDAR HAC / NEWEY-WEST
# ============================================================

for variable in ["diferencia_roa", "diferencia_roe"]:

    y = comparacion[variable].dropna()

    # Una constante permite estimar la diferencia promedio
    X = sm.add_constant(pd.DataFrame(index=y.index))

    modelo = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": 12}
    )

    print(f"\nRESULTADO HAC - {variable.upper()}")
    print(f"Diferencia promedio: {modelo.params['const']:.4f}")
    print(f"Error estándar HAC: {modelo.bse['const']:.4f}")
    print(f"Estadístico t: {modelo.tvalues['const']:.4f}")
    print(f"Valor p: {modelo.pvalues['const']:.6f}")
    print(
        f"IC 95%: "
        f"[{modelo.conf_int().loc['const', 0]:.4f}, "
        f"{modelo.conf_int().loc['const', 1]:.4f}]"
    )

    # ============================================================
# PRUEBA DE ROBUSTEZ HAC CON DIFERENTES REZAGOS
# ============================================================

rezagos = [3, 6, 12, 18, 24]

print("\nPRUEBA DE ROBUSTEZ HAC")

for variable in ["diferencia_roa", "diferencia_roe"]:

    y = comparacion[variable].dropna()
    X = sm.add_constant(pd.DataFrame(index=y.index))

    print(f"\n{variable.upper()}")

    for rezago in rezagos:

        modelo_robusto = sm.OLS(y, X).fit(
            cov_type="HAC",
            cov_kwds={"maxlags": rezago}
        )

        print(
            f"Rezago {rezago:>2}: "
            f"coef={modelo_robusto.params['const']:.4f}, "
            f"EE={modelo_robusto.bse['const']:.4f}, "
            f"p={modelo_robusto.pvalues['const']:.6f}"
        )