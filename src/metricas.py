import pandas as pd


def resumen_general(df):
    return {
        "total_usuarios": len(df),
        "usuarios_unicos": df["user"].nunique()
    }


def modalidad(df):
    resultado = (
        df["modalidad"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )
    resultado.columns = ["modalidad", "count"]
    return resultado


def disponibilidad(df):
    resultado = (
        df["disponibilidad"]
        .fillna("Sin dato")
        .value_counts()
        .reset_index()
    )
    resultado.columns = ["disponibilidad", "count"]
    return resultado


def profesiones(df, top=20):
    resultado = (
        df["profession"]
        .fillna("Sin dato")
        .value_counts()
        .head(top)
        .reset_index()
    )
    resultado.columns = ["profession", "count"]
    return resultado


def ubicaciones(df, top=20):
    resultado = (
        df["location"]
        .fillna("Sin dato")
        .value_counts()
        .head(top)
        .reset_index()
    )
    resultado.columns = ["location", "count"]
    return resultado


def modalidad_profesion(df):
    return pd.crosstab(
        df["modalidad"],
        df["profession"]
    )


def disponibilidad_profesion(df):
    return pd.crosstab(
        df["disponibilidad"],
        df["profession"]
    )


def top_rubros(df, top=20):
    df_rubros = df.explode("rubros")
    resultado = (
        df_rubros["rubros"]
        .fillna("Sin dato")
        .value_counts()
        .head(top)
        .reset_index()
    )
    resultado.columns = ["rubro", "count"]
    return resultado