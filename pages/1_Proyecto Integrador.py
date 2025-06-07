import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Gestión de Eventos Escolares", layout="wide")
st.title("🏫 Gestión de Eventos Escolares")

# URLs de la API (DEBEN ser consistentes con los nombres usados en cargar_datos)
API_ENDPOINTS = {
    "estudiantes": "https://eventos-25.onrender.com/api/estudiantes",
    "asistenciaeventos": "https://eventos-25.onrender.com/api/asistenciaeventos",
    "eventos": "https://eventos-25.onrender.com/api/eventos",
    "categoriaevento": "https://eventos-25.onrender.com/api/categoriasevento", # <-- ¡CORRECCIÓN AQUÍ! Mantenemos "categoriaevento" (singular)
    "participantes": "https://eventos-25.onrender.com/api/participantes",
    "profesores" : "https://eventos-25.onrender.com/api/profesores",
}

@st.cache_data(ttl=300)  # Cache de 5 minutos
def cargar_datos(tipo):
    try:
        response = requests.get(API_ENDPOINTS[tipo], timeout=30)
        response.raise_for_status() # Lanza un error para códigos de estado HTTP 4xx/5xx
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error de red o API al cargar {tipo}: {str(e)}")
        return pd.DataFrame()
    except ValueError as e: # Para errores si la respuesta no es JSON
        st.error(f"Error al decodificar JSON para {tipo}: {str(e)}. La API podría no estar devolviendo JSON válido.")
        return pd.DataFrame()
    except KeyError as e: # Específicamente para el error de clave no encontrada
        st.error(f"Error: La clave '{tipo}' no se encontró en API_ENDPOINTS. Revise la consistencia de los nombres. Detalle: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado al cargar {tipo}: {str(e)}")
        return pd.DataFrame()

# Mostrar el código de la función cargar_datos si el usuario lo desea
with st.expander("📄 Ver código de la función cargar_datos", expanded=False):
    # Ya no es necesario el if st.button("Mostrar código fuente"):
    # ya que el código se muestra cuando el expander está abierto.
    st.code('''import streamlit as st
import requests
import pandas as pd
from datetime import datetime
@st.cache_data(ttl=300)  # Cache de 5 minutos
def cargar_datos(tipo):
    try:
        response = requests.get(API_ENDPOINTS[tipo], timeout=30)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e: # Una excepción más general para captura, pero las específicas son mejores
        st.error(f"Error al cargar {tipo}: {str(e)}")
        return pd.DataFrame()''', language='python')


# Cargar todos los datos
with st.spinner("Cargando datos del evento..."):
    # ¡CORRECCIÓN AQUÍ! Llamada ahora es "categoriaevento" (singular)
    estudiantes_df = cargar_datos("estudiantes")
    asistenciaeventos_df = cargar_datos("asistenciaeventos")
    eventos_df = cargar_datos("eventos")
    categoriaevento_df = cargar_datos("categoriaevento") # <--- ¡CORREGIDO AQUI!
    participantes_df = cargar_datos("participantes")
    profesores_df = cargar_datos("profesores")

# Sidebar con selección de tabla principal
st.sidebar.header("🔍 Filtros Principales")
tabla_seleccionada = st.sidebar.selectbox(
    "Seleccionar tabla para visualizar",
    options=["Estudiantes", "Eventos", "Profesores", "Asistencia Eventos", "Categoria Evento", "Participantes"],
    index=0
)

# Función para mostrar tabla con filtros
def mostrar_tabla(titulo, df, columnas_filtro):
    st.header(f"📋 {titulo}")
    
    if df.empty:
        st.warning(f"No hay datos de {titulo.lower()} disponibles o hubo un error al cargarlos.")
        return
    
    # Filtros dinámicos
    df_filtrado = df.copy()
    with st.expander("⚙️ Filtros Avanzados", expanded=False):
        # Aumentar el número de columnas para los filtros para evitar desbordamiento
        # y usar el mínimo entre el número de filtros y un número fijo (ej. 4)
        cols = st.columns(min(len(columnas_filtro), 4))
        filtros = {}
        
        for i, col in enumerate(columnas_filtro):
            if col in df.columns:
                with cols[i % len(cols)]: # Distribuye los filtros equitativamente
                    # Asegúrate de que cada selectbox/slider/date_input tenga una clave única
                    widget_key = f"{titulo}_{col}_{i}" 
                    
                    if pd.api.types.is_object_dtype(df[col]): # Cadenas/categorías
                        options = ['Todos'] + sorted(df[col].dropna().unique().tolist())
                        seleccion = st.selectbox(f"Filtrar por {col}", options, key=f"sb_{widget_key}")
                        if seleccion != 'Todos':
                            filtros[col] = seleccion
                    elif pd.api.types.is_numeric_dtype(df[col]): # Números
                        min_val = float(df[col].min())
                        max_val = float(df[col].max())
                        seleccion = st.slider(f"Rango de {col}", min_val, max_val, (min_val, max_val), key=f"sl_{widget_key}")
                        filtros[col] = seleccion
                    elif pd.api.types.is_datetime64_any_dtype(df[col]): # Fechas
                        # Asegurarse de que la columna es de tipo datetime
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        df_valid_dates = df.dropna(subset=[col])
                        if not df_valid_dates.empty:
                            min_date = df_valid_dates[col].min().date()
                            max_date = df_valid_dates[col].max().date()
                            date_range = st.date_input(f"Rango de fechas para {col}", 
                                                      value=(min_date, max_date), 
                                                      min_value=min_date, 
                                                      max_value=max_date,
                                                      key=f"dt_{widget_key}")
                            if len(date_range) == 2:
                                filtros[col] = (pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]).replace(hour=23, minute=59, second=59))
            else:
                st.warning(f"La columna de filtro '{col}' no existe en la tabla '{titulo}'.")
    
    # Aplicar filtros
    for col, val in filtros.items():
        if isinstance(val, tuple) and (pd.api.types.is_numeric_dtype(df_filtrado[col]) or pd.api.types.is_datetime64_any_dtype(df_filtrado[col])):
            df_filtrado = df_filtrado[(df_filtrado[col] >= val[0]) & (df_filtrado[col] <= val[1])]
        else:
            df_filtrado = df_filtrado[df_filtrado[col] == val]
    
    # Mostrar datos
    st.dataframe(df_filtrado, height=500, use_container_width=True)
    
    # Estadísticas
    st.subheader("📊 Estadísticas")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df)) # Mostrar total sin filtrar
    with col2:
        st.metric("Registros Filtrados", len(df_filtrado))
    with col3:
        # Intenta encontrar una columna de fecha para la última actualización
        date_cols = [col for col in df_filtrado.columns if 'fecha' in col.lower() and pd.api.types.is_datetime64_any_dtype(df_filtrado[col])]
        if date_cols and not df_filtrado.empty:
            latest_date = pd.to_datetime(df_filtrado[date_cols[0]], errors='coerce').max()
            if pd.notna(latest_date):
                st.metric("Fecha Más Reciente", latest_date.strftime('%Y-%m-%d'))
            else:
                st.metric("Fecha Más Reciente", "N/A")
        else:
            st.metric("Fecha Más Reciente", "N/A (No hay columna de fecha)")
    
    # Exportar
    if not df_filtrado.empty:
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            f"⬇️ Exportar {titulo} como CSV",
            data=csv,
            file_name=f"{titulo.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos filtrados para exportar.")


# Visualización según selección
if tabla_seleccionada == "Estudiantes":
    mostrar_tabla(
        "Estudiantes",
        estudiantes_df,
        ["nombre", "apellido", "correo", "carrera", "semestre", "grado", "grupo", "fechaNacimiento"]
    )

elif tabla_seleccionada == "Eventos":
    mostrar_tabla(
        "Eventos",
        eventos_df,
        ["nombre_evento", "fecha_evento", "ubicacion", "id_categoria_evento", "cupo_maximo", "fecha_inicio", "fecha_fin" , "categoria_evento"]
    )

elif tabla_seleccionada == "Profesores":
    mostrar_tabla(
        "Profesores",
        profesores_df,
        ["nombre", "apellido", "email", "departamento", "especialidad"]
    )

elif tabla_seleccionada == "Asistencia Eventos":
    mostrar_tabla(
        "Asistencia a Eventos",
        asistenciaeventos_df,
        ["id_evento", "id_participante", "fecha_asistencia"]
    )

elif tabla_seleccionada == "Categoria Evento":
    mostrar_tabla(
        "Categoria de Evento",
        categoriaevento_df, # <--- ¡CORREGIDO AQUI! La variable ahora es 'categoriaevento_df'
        ["nombre_categoria", "descripcion"]
    )

elif tabla_seleccionada == "Participantes":
    mostrar_tabla(
        "Participantes",
        participantes_df,
        ["id_evento", "id_estudiante", "rol", "fecha_registro"]
    )

# Actualización manual de datos
if st.sidebar.button("🔄 Actualizar Todos los Datos"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")