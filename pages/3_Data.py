import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid

# Configuración de la página
st.set_page_config(page_title="Tablero de Registro de Carros Eléctricos", layout="wide")

# CSS personalizado para estilos
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stSidebar {background-color: black;}
    .stTitle {color: #1f77b4; font-size: 2.5em;}
    .stSubheader {color: #ff7f0e;}
    .stButton>button {background-color: #2ca02c; color: white;}
    .stSelectbox, .stMultiselect, .stSlider {background-color: black;}
    </style>
""", unsafe_allow_html=True)

# Cargar el dataset
@st.cache_data
def load_data():
    df = pd.read_csv("static/datasets/registros_carros_electricos.csv")
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
    return df

df = load_data()

# Barra lateral para filtros
st.sidebar.header("Opciones de Filtro")

# Filtro por lugar
lugares = sorted(df["lugar_registro"].unique())
selected_lugares = st.sidebar.multiselect("Selecciona Lugar(es)", lugares, default=lugares[:3])

# Filtro por marca de auto
marcas = sorted(df["marca_auto"].unique())
selected_marcas = st.sidebar.multiselect("Selecciona Marca(s) de Auto", marcas, default=marcas[:3])

# Filtro por año de modelo
min_year, max_year = int(df["año_modelo"].min()), int(df["año_modelo"].max())
selected_years = st.sidebar.slider("Selecciona Rango de Año de Modelo", min_year, max_year, (min_year, max_year))

# Filtro por edad
min_age, max_age = int(df["edad"].min()), int(df["edad"].max())
selected_age = st.sidebar.slider("Selecciona Rango de Edad", min_age, max_age, (min_age, max_age))

# Filtro por autonomía
min_autonomy, max_autonomy = int(df["autonomia_km"].min()), int(df["autonomia_km"].max())
selected_autonomy = st.sidebar.slider("Selecciona Rango de Autonomía (km)", min_autonomy, max_autonomy, (min_autonomy, max_autonomy))

# Filtro por tipo de carga
tipos_carga = sorted(df["tipo_carga"].unique())
selected_tipos_carga = st.sidebar.multiselect("Selecciona Tipo(s) de Carga", tipos_carga, default=tipos_carga)

# Filtro por baterías recicladas
baterias = df["baterias_recicladas"].unique()
selected_baterias = st.sidebar.multiselect("Baterías Recicladas", baterias, default=baterias)

# Aplicar filtros
filtered_df = df[
    (df["lugar_registro"].isin(selected_lugares)) &
    (df["marca_auto"].isin(selected_marcas)) &
    (df["año_modelo"].between(selected_years[0], selected_years[1])) &
    (df["edad"].between(selected_age[0], selected_age[1])) &
    (df["autonomia_km"].between(selected_autonomy[0], selected_autonomy[1])) &
    (df["tipo_carga"].isin(selected_tipos_carga)) &
    (df["baterias_recicladas"].isin(selected_baterias))
]

# Contenido principal
st.title("Tablero de Registro de Carros Eléctricos")
st.markdown("Explora y analiza los registros de carros eléctricos con filtros y visualizaciones interactivas.")

# Métricas clave
col1, col2, col3 = st.columns(3)
col1.metric("Total de Registros", len(filtered_df))
col2.metric("Autonomía Promedio (km)", round(filtered_df["autonomia_km"].mean(), 1))
col3.metric("Edad Promedio", round(filtered_df["edad"].mean(), 1))

# Visualizaciones
st.subheader("Visualizaciones de Datos")

# Gráfico de pastel: Distribución de marcas de autos
fig_pie = px.pie(filtered_df, names="marca_auto", title="Distribución de marcas de autos eléctricos",
                 color_discrete_sequence=px.colors.qualitative.Bold)
fig_pie.update_layout(font_size=12)
st.plotly_chart(fig_pie, use_container_width=True)

# Histograma: Distribución de edades
fig_hist = px.histogram(filtered_df, x="edad", nbins=20, title="Distribución de edades de los propietarios",
                        color_discrete_sequence=["#ff7f0e"])
fig_hist.update_layout(font_size=12, xaxis_title="Edad", yaxis_title="Cantidad")
st.plotly_chart(fig_hist, use_container_width=True)

# Gráfico de barras: Autonomía promedio por marca
avg_autonomy = filtered_df.groupby("marca_auto")["autonomia_km"].mean().reset_index()
fig_bar = px.bar(
    avg_autonomy,
    x="marca_auto",
    y="autonomia_km",
    title="Autonomía promedio por marca",
    color="marca_auto",
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={"marca_auto": "Marca", "autonomia_km": "Autonomía promedio (km)"}
)
fig_bar.update_layout(font_size=12, xaxis_title="Marca", yaxis_title="Autonomía promedio (km)")
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de líneas: Registros a lo largo del tiempo
filtered_df["year_month"] = filtered_df["fecha_registro"].dt.to_period("M").astype(str)
registrations_over_time = filtered_df.groupby("year_month").size().reset_index(name="count")
fig_line = px.line(registrations_over_time, x="year_month", y="count", title="Registros a lo largo del tiempo",
                   markers=True, color_discrete_sequence=["#2ca02c"])
fig_line.update_layout(font_size=12, xaxis_title="Año-Mes", yaxis_title="Número de registros")
st.plotly_chart(fig_line, use_container_width=True)

# Tabla de datos
st.subheader("Tabla de Datos Filtrados")
st.dataframe(filtered_df.drop(columns=["year_month"] if "year_month" in filtered_df.columns else []), height=400)

# Dato interesante
st.subheader("Dato Interesante")
most_common_brand = filtered_df["marca_auto"].mode()[0]
st.markdown(f"La marca de auto más popular en el conjunto de datos filtrado es **{most_common_brand}**, ¡lo que refleja su fuerte presencia en el mercado de vehículos eléctricos en las regiones seleccionadas!")