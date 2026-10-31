import streamlit as st
import pandas as pd

from config import *
from src.cargar_datos import build_all, load_df_cache
from src import metricas
from src import graficos


# ==================================
# CONFIGURACIÓN GENERAL
# ==================================

st.set_page_config(
    page_title="Laboral.AI Talent Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================
# ESTILO
# ==================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    font-size: 2rem;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def cargar_datos():

    usuarios_path = os.path.join(
        CACHE_DIR,
        "Usuarios_Master.csv"
    )

    # Intentar leer cache
    try:

        if os.path.exists(usuarios_path):

            return load_df_cache(
                usuarios_path,
                con_fecha=False
            )

    except Exception as e:

        st.warning(
            f"No se pudo leer cache: {e}"
        )

    # Si falla → Mongo
    try:
        return build_all(DB_NAME, MONGO_URI, cache_dir=CACHE_DIR)
    except Exception as e:
        st.error(f"Error al cargar datos desde Mongo: {e}")
        return pd.DataFrame()

# ==================================
# HEADER
# ==================================

st.title("📊 Laboral.AI Talent Dashboard")
st.caption("Análisis de candidatos activos con invitationCode válido")

st.divider()

# ==================================
# SIDEBAR
# ==================================

st.sidebar.header("Filtros")

cargar_datos.clear()
df = build_all(DB_NAME, MONGO_URI, cache_dir=CACHE_DIR)
print(df.columns.tolist())

modalidades = sorted(
    df["modalidad"]
    .dropna()
    .unique()
)

profesiones = sorted(
    df["profession"]
    .dropna()
    .unique()
)

ubicaciones = sorted(
    df["location"]
    .dropna()
    .unique()
)

disponibilidades = sorted(
    df["disponibilidad"]
    .dropna()
    .unique()
)

modalidad = st.sidebar.multiselect(
    "Modalidad",
    modalidades
)

profesion = st.sidebar.multiselect(
    "Profesión",
    profesiones
)

ubicacion = st.sidebar.multiselect(
    "Ubicación",
    ubicaciones
)

disponibilidad = st.sidebar.multiselect(
    "Disponibilidad",
    disponibilidades
)

# ==================================
# FILTROS
# ==================================

df_filtrado = df.copy()

if modalidad:
    df_filtrado = df_filtrado[
        df_filtrado["modalidad"].isin(modalidad)
    ]

if profesion:
    df_filtrado = df_filtrado[
        df_filtrado["profession"].isin(profesion)
    ]

if ubicacion:
    df_filtrado = df_filtrado[
        df_filtrado["location"].isin(ubicacion)
    ]

if disponibilidad:
    df_filtrado = df_filtrado[
        df_filtrado["disponibilidad"].isin(disponibilidad)
    ]

# ==================================
# KPI PRINCIPALES
# ==================================

resumen = metricas.resumen_general(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Usuarios",
        resumen["total_usuarios"]
    )

with col2:
    st.metric(
        "Usuarios únicos",
        resumen["usuarios_unicos"]
    )

with col3:
    st.metric(
        "Profesiones",
        df_filtrado["profession"].nunique()
    )

with col4:
    st.metric(
        "Ubicaciones",
        df_filtrado["location"].nunique()
    )

# ==================================
# TABLAS MÉTRICAS
# ==================================

df_modalidad = metricas.modalidad(df_filtrado)
df_disponibilidad = metricas.disponibilidad(df_filtrado)
df_profesiones = metricas.profesiones(df_filtrado)
df_rubros = metricas.top_rubros(df_filtrado)
df_ubicaciones = metricas.ubicaciones(df_filtrado)

# ==================================
# FILA 1
# ==================================

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        graficos.modalidad(df_modalidad),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        graficos.disponibilidad(df_disponibilidad),
        use_container_width=True
    )

# ==================================
# FILA 2
# ==================================

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        graficos.profesiones(df_profesiones),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        graficos.rubros(df_rubros),
        use_container_width=True
    )

# ==================================
# FILA 3
# ==================================

st.plotly_chart(
    graficos.ubicaciones(df_ubicaciones),
    use_container_width=True
)

# ==================================
# TABLA DETALLE
# ==================================

with st.expander("Ver registros"):

    columnas = [
        "firstName",
        "lastName",
        "profession",
        "modalidad",
        "disponibilidad",
        "location"
    ]

    columnas = [
        c for c in columnas
        if c in df_filtrado.columns
    ]

    st.dataframe(
        df_filtrado[columnas],
        use_container_width=True
    )