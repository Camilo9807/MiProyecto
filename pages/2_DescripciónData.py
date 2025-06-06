import streamlit as st

st.title("Guía del Dashboard de Autos Eléctricos 🚗⚡")
st.markdown("""
<style>
.big-font {font-size: 1.4em;}
hr {margin-top: 1em; margin-bottom: 1em;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-font">
<strong>¿Qué es este Dashboard?</strong><br>
Es una herramienta interactiva que te permite explorar los registros de autos eléctricos mediante gráficos y filtros personalizados.
</div>
<hr>
""", unsafe_allow_html=True)

st.subheader("Filtros disponibles")
st.markdown("""
- **Lugar de registro**: Ciudad o región donde se registró el auto.
- **Marca de auto**: Selecciona una o varias marcas.
- **Año del modelo**: Rango de años del modelo del auto.
- **Edad**: Rango de edad del propietario.
- **Autonomía (km)**: Rango de autonomía máxima del auto.
- **Tipo de carga**: Tipo de carga compatible (rápida, lenta, etc.).
- **Baterías recicladas**: Filtra autos que usan o no baterías recicladas.
""")

st.subheader("Columnas de la base de datos")
st.table([
    ["fecha_registro", "Fecha de registro del auto (datetime)"],
    ["lugar_registro", "Ciudad/región del registro (texto)"],
    ["marca_auto", "Marca del auto eléctrico (texto)"],
    ["año_modelo", "Año del modelo (entero)"],
    ["edad", "Edad del propietario (entero)"],
    ["autonomia_km", "Autonomía máxima (km) (número)"],
    ["tipo_carga", "Tipo de carga compatible (texto)"],
    ["baterias_recicladas", "¿Usa baterías recicladas? (Sí/No)"]
])

st.subheader("¿Qué puedes visualizar?")
st.markdown("""
- **Métricas clave:** Total de registros, autonomía promedio y edad promedio.
- **Gráfica de pastel:** Distribución de registros por marca.
- **Histograma:** Distribución de la edad de propietarios.
- **Barras:** Autonomía promedio por marca.
- **Línea:** Evolución de registros en el tiempo.
- **Tabla:** Datos filtrados en detalle.
""")

st.info("¡Explora los filtros y descubre tendencias interesantes del mercado de autos eléctricos!")