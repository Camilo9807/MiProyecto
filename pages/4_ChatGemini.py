import streamlit as st # type: ignore
from google import genai

# Configuración de la página
st.set_page_config(page_title="Chat Básico con Gemini", layout="centered")
st.title("💬 Chat con Gemini")
st.markdown("Ingresa un tema o pregunta para obtener una respuesta generada por Gemini.")

# Interfaz de usuario
prompt = st.text_input("Escribe tu pregunta o tema:", placeholder="Ej. Explica cómo funciona la IA en pocas palabras")
enviar = st.button("Generar Respuesta")

# Función que usa el código original
def generar_respuesta(prompt):
    if not prompt:
        return "Por favor, ingresa un tema o pregunta."
    try:
        client = genai.Client(api_key="AIzaSyA8y8Eb6_DccDP9EH8V5IGDGkdt6ehimPs")  # Código original
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt  # Código original con prompt dinámico
        )
        return response.text  # Código original
    except Exception as e:
        return f"Error: {str(e)}"

# Lógica principal
if enviar and prompt:
    with st.spinner("Generando respuesta..."):
        respuesta = generar_respuesta(prompt)
        st.subheader("Respuesta:")
        st.markdown(respuesta)
else:
    st.info("Escribe un tema o pregunta y haz clic en Generar Respuesta.")