import plotly.express as px
import plotly.graph_objects as go


# =========================
# MODALIDAD
# =========================

def modalidad(df_modalidad):
    fig = px.pie(
        df_modalidad,
        names="modalidad",
        values="count",
        title="Modalidad de trabajo"
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}<br>Usuarios: %{value}<extra></extra>"
    )
    return fig


# =========================
# DISPONIBILIDAD
# =========================

def disponibilidad(df_disponibilidad):
    fig = px.bar(
        df_disponibilidad,
        x="disponibilidad",
        y="count",
        title="Disponibilidad"
    )

    fig.update_layout(
        xaxis_title="Disponibilidad",
        yaxis_title="Usuarios",
        hovermode="x unified"
    )

    fig.update_traces(
        hovertemplate="Disponibilidad: %{x}<br>Usuarios: %{y}<extra></extra>"
    )
    return fig


# =========================
# PROFESIONES
# =========================

def profesiones(df_profesiones):
    fig = px.bar(
        df_profesiones,
        x="count",
        y="profession",
        orientation="h",
        title="Top Profesiones"
    )

    fig.update_layout(
        xaxis_title="Usuarios",
        yaxis_title="Profesión",
        yaxis={"categoryorder": "total ascending"}
    )

    fig.update_traces(
        hovertemplate="Profesión: %{y}<br>Usuarios: %{x}<extra></extra>"
    )
    return fig


# =========================
# UBICACIONES
# =========================

def ubicaciones(df_ubicacion):
    fig = px.bar(
        df_ubicacion,
        x="count",
        y="location",
        orientation="h",
        title="Top Ubicaciones"
    )

    fig.update_layout(
        xaxis_title="Usuarios",
        yaxis_title="Ubicación",
        yaxis={"categoryorder": "total ascending"}
    )

    fig.update_traces(
        hovertemplate="Ubicación: %{y}<br>Usuarios: %{x}<extra></extra>"
    )
    return fig


# =========================
# RUBROS
# =========================

def rubros(df_rubros):
    fig = px.bar(
        df_rubros,
        x="count",
        y="rubro",
        orientation="h",
        title="Top Rubros"
    )

    fig.update_layout(
        xaxis_title="Usuarios",
        yaxis_title="Rubro",
        yaxis={"categoryorder": "total ascending"}
    )

    fig.update_traces(
        hovertemplate="Rubro: %{y}<br>Usuarios: %{x}<extra></extra>"
    )
    return fig


# =========================
# MODALIDAD VS PROFESIÓN
# =========================

def modalidad_profesion(df_modalidad_profesion):
    fig = px.imshow(
        df_modalidad_profesion,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Modalidad vs Profesión"
    )

    fig.update_layout(
        xaxis_title="Profesión",
        yaxis_title="Modalidad"
    )
    return fig


# =========================
# DISPONIBILIDAD VS PROFESIÓN
# =========================

def disponibilidad_profesion(df_disponibilidad_profesion):
    fig = px.imshow(
        df_disponibilidad_profesion,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Greens",
        title="Disponibilidad vs Profesión"
    )

    fig.update_layout(
        xaxis_title="Profesión",
        yaxis_title="Disponibilidad"
    )
    return fig
