# inicio.py
import streamlit as st

# Configuración de la página de Streamlit
# Ancho de la página y título
st.set_page_config(
    page_title="Portanda de Proyecto",
    layout="centered", # 'centered' o 'wide'
    initial_sidebar_state="collapsed" # Oculta la barra lateral por defecto
)

# Estilo personalizado para el fondo degradado y la fuente
# Streamlit permite inyectar CSS directamente
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        /* Establece un degradado de fondo que ocupa toda la pantalla */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .st-emotion-cache-1f1jys-Title { /* Selector para el título principal */
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); /* Efecto de sombra para el texto */
    }

    .st-emotion-cache-nahz7x { /* Selector para el subtítulo/descripción */
        color: white;
        opacity: 0.9;
    }

    .st-emotion-cache-k7vsyb { /* Selector para subtítulos de sección */
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .st-emotion-cache-cnjs7c { /* Selector para st.markdown content */
        color: white;
    }

    /* Estilo para el contenedor principal de la portada */
    .st-emotion-cache-eczf16 { /* Selector para st.container */
        background-color: rgba(255, 255, 255, 0.2); /* Fondo blanco transparente */
        backdrop-filter: blur(10px); /* Efecto de desenfoque de fondo */
        border-radius: 24px; /* Bordes redondeados */
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); /* Sombra más pronunciada */
        border: 1px solid rgba(255, 255, 255, 0.3); /* Borde semitransparente */
        padding: 3rem 4rem; /* Relleno aumentado */
        text-align: center;
        max-width: 960px; /* Ancho máximo */
        margin: auto;
    }

    /* Estilo para los elementos de la lista de integrantes */
    .st-emotion-cache-fybf1q { /* Selector para st.columns dentro del contenedor */
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 0.75rem; /* Espacio entre elementos */
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    .st-emotion-cache-fybf1q:hover {
        transform: scale(1.03); /* Efecto de escala al pasar el ratón */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Centrar el contenido del contenedor */
    [data-testid="stVerticalBlock"] > div:first-child {
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título del Proyecto
st.title("Proyecto Integrador")

# Breve Descripción del Proyecto
st.markdown(
    """
    Este proyecto tiene como objetivo principal la investigación y el desarrollo de una solución innovadora para la gestión y análisis de datos en entornos dinámicos, aplicando principios de inteligencia artificial y machine learning para optimizar la toma de decisiones y mejorar la eficiencia operativa.
    """
)

# Sección de Integrantes
st.subheader("Integrantes del Equipo")

# Lista de integrantes
integrantes = [
    "Juan Diego Palacio",
    "Dunier Camilo Galvis",
    "Daniela Mejia"
]

# Mostrar cada integrante como un elemento de lista estilizado
for integrante in integrantes:
    st.markdown(
        f"""
        <div class="st-emotion-cache-fybf1q">
            {integrante}
        </div>
        """,
        unsafe_allow_html=True
    )

# Pie de Página
st.markdown(
    """
    <div style="text-align: center; margin-top: 4rem; opacity: 0.8; font-size: 0.9rem;">
        Desarrollado para la materia de Proyecto Integrador - 2025
    </div>
    """,
    unsafe_allow_html=True
)
