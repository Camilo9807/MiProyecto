import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid

# Set page configuration for a wide layout and custom title
st.set_page_config(page_title="Electric Car Registry Dashboard", layout="wide")

# Custom CSS for styling
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

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("static/datasets/registros_carros_electricos.csv")
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
    return df

df = load_data()

# Sidebar for filters
st.sidebar.header("Filter Options")

# Filter by location
lugares = sorted(df["lugar_registro"].unique())
selected_lugares = st.sidebar.multiselect("Select Location(s)", lugares, default=lugares[:3])

# Filter by car brand
marcas = sorted(df["marca_auto"].unique())
selected_marcas = st.sidebar.multiselect("Select Car Brand(s)", marcas, default=marcas[:3])

# Filter by model year
min_year, max_year = int(df["año_modelo"].min()), int(df["año_modelo"].max())
selected_years = st.sidebar.slider("Select Model Year Range", min_year, max_year, (min_year, max_year))

# Filter by age
min_age, max_age = int(df["edad"].min()), int(df["edad"].max())
selected_age = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Filter by autonomy
min_autonomy, max_autonomy = int(df["autonomia_km"].min()), int(df["autonomia_km"].max())
selected_autonomy = st.sidebar.slider("Select Autonomy Range (km)", min_autonomy, max_autonomy, (min_autonomy, max_autonomy))

# Filter by charging type
tipos_carga = sorted(df["tipo_carga"].unique())
selected_tipos_carga = st.sidebar.multiselect("Select Charging Type(s)", tipos_carga, default=tipos_carga)

# Filter by recycled batteries
baterias = df["baterias_recicladas"].unique()
selected_baterias = st.sidebar.multiselect("Recycled Batteries", baterias, default=baterias)

# Apply filters
filtered_df = df[
    (df["lugar_registro"].isin(selected_lugares)) &
    (df["marca_auto"].isin(selected_marcas)) &
    (df["año_modelo"].between(selected_years[0], selected_years[1])) &
    (df["edad"].between(selected_age[0], selected_age[1])) &
    (df["autonomia_km"].between(selected_autonomy[0], selected_autonomy[1])) &
    (df["tipo_carga"].isin(selected_tipos_carga)) &
    (df["baterias_recicladas"].isin(selected_baterias))
]

# Main content
st.title("Electric Car Registry Dashboard")
st.markdown("Explore and analyze electric car registrations with interactive filters and visualizations.")

# Display key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Registrations", len(filtered_df))
col2.metric("Average Autonomy (km)", round(filtered_df["autonomia_km"].mean(), 1))
col3.metric("Average Age", round(filtered_df["edad"].mean(), 1))

# Visualizations
st.subheader("Data Visualizations")

# Pie chart: Distribution of car brands
fig_pie = px.pie(filtered_df, names="marca_auto", title="Distribution of Car Brands",
                 color_discrete_sequence=px.colors.qualitative.Bold)
fig_pie.update_layout(font_size=12)
st.plotly_chart(fig_pie, use_container_width=True)

# Histogram: Age distribution
fig_hist = px.histogram(filtered_df, x="edad", nbins=20, title="Age Distribution of Owners",
                        color_discrete_sequence=["#ff7f0e"])
fig_hist.update_layout(font_size=12, xaxis_title="Age", yaxis_title="Count")
st.plotly_chart(fig_hist, use_container_width=True)

# Bar chart: Average autonomy by brand
avg_autonomy = filtered_df.groupby("marca_auto")["autonomia_km"].mean().reset_index()
fig_bar = px.bar(avg_autonomy, x="marca_auto", y="autonomia_km", title="Average Autonomy by Brand",
                 color="marca_auto", color_discrete_sequence=px.colors.qualitative.Set2)
fig_bar.update_layout(font_size=12, xaxis_title="Brand", yaxis_title="Average Autonomy (km)")
st.plotly_chart(fig_bar, use_container_width=True)

# Line chart: Registrations over time
filtered_df["year_month"] = filtered_df["fecha_registro"].dt.to_period("M").astype(str)
registrations_over_time = filtered_df.groupby("year_month").size().reset_index(name="count")
fig_line = px.line(registrations_over_time, x="year_month", y="count", title="Registrations Over Time",
                   markers=True, color_discrete_sequence=["#2ca02c"])
fig_line.update_layout(font_size=12, xaxis_title="Year-Month", yaxis_title="Number of Registrations")
st.plotly_chart(fig_line, use_container_width=True)

# Data table
st.subheader("Filtered Data Table")
st.dataframe(filtered_df.drop(columns=["year_month"] if "year_month" in filtered_df.columns else []), height=400)

# Interesting fact
st.subheader("Interesting Fact")
most_common_brand = filtered_df["marca_auto"].mode()[0]
st.markdown(f"The most popular car brand in the filtered dataset is **{most_common_brand}**, reflecting its strong presence in the electric vehicle market in the selected regions!")