import streamlit as st
from google import genai

# --- Configuración de la Aplicación ---
st.set_page_config(page_title="Moto-Chat con Gemini", layout="centered")
st.title("🏍️ Moto-Chat: Tu Experto en Dos Ruedas")
st.markdown("¡Pregúntale a Gemini cualquier cosa sobre **motos**! Si tu pregunta no es sobre motos, te lo haré saber.")

# --- Interfaz de Usuario ---
# Campo de entrada para la pregunta del usuario
user_query = st.text_input("Escribe tu pregunta sobre motos:", placeholder="Ej. ¿Cuál es la diferencia entre una moto naked y una sport?")

# Botón para enviar la pregunta
submit_button = st.button("Generar Respuesta")

# --- Función para Generar Respuesta con Gemini ---
def get_gemini_response(prompt_text):
    """
    Genera una respuesta utilizando el modelo Gemini, con un enfoque en motos.
    """
    if not prompt_text:
        return "Por favor, ingresa una pregunta para que pueda ayudarte."

    try:
        # Aquí se usa una API Key de ejemplo. ¡Recuerda reemplazarla con la tuya!
        # Por seguridad, no es recomendable dejar la API Key directamente en el código
        # en una aplicación desplegada. Considera usar variables de entorno.
        client = genai.Client(api_key="AIzaSyA8y8Eb6_DccDP9EH8V5IGDGkdt6ehimPs")

        # Añadimos una instrucción al prompt para que el modelo se enfoque en motos.
        # Esto no garantiza al 100% que solo hable de motos, pero ayuda a guiarlo.
        system_instruction = "Eres un experto en motos. Responde únicamente preguntas sobre motos. Si la pregunta no es sobre motos, indica amablemente que solo puedes hablar de ese tema."
        
        full_prompt = f"{system_instruction}\n\nPregunta del usuario: {prompt_text}"

        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=full_prompt 
        )
        return response.text
    except Exception as e:
        return f"Ups, algo salió mal: {str(e)}. Por favor, inténtalo de nuevo más tarde."

# --- Lógica Principal de la Aplicación ---
if submit_button and user_query:
    with st.spinner("Buscando la respuesta en el garaje virtual..."):
        # Generar la respuesta usando la función definida
        response_text = get_gemini_response(user_query)
        
        # Mostrar la respuesta al usuario
        st.subheader("Respuesta de Moto-Chat:")
        st.markdown(response_text)
elif submit_button and not user_query:
    st.info("Por favor, escribe tu pregunta antes de presionar 'Generar Respuesta'.")
else:
    st.info("¡Anímate a preguntar! Estoy aquí para ayudarte con tus dudas sobre motos.")