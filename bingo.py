import streamlit as st
import time
from gtts import gTTS
from io import BytesIO
import base64


# Función para reproducir la voz
def reproducir_voz(texto):
    tts = gTTS(text=texto, lang='es')
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    audio_data = buffer.read()
    base64_audio = base64.b64encode(audio_data).decode()
    st.audio(f"data:audio/ogg;base64,{base64_audio}", format='audio/ogg')

# Función para generar un número aleatorio usando el método proporcionado
def generar_numero_aleatorio(lim_inferior, lim_superior, numeros_extraidos):
    Xo = int(time.time())
    a = 1103515245
    c = 12345
    m = 32768

    while True:
        Xn = (a * Xo + c) % m
        numero_aleatorio = lim_inferior + (Xn * (lim_superior - lim_inferior) // m)
        if numero_aleatorio not in numeros_extraidos:
            numeros_extraidos.add(numero_aleatorio)
            return numero_aleatorio, numeros_extraidos
        Xo = Xn

# Función para obtener la letra correspondiente al número
def obtener_letra(numero):
    if numero <= 15:
        return 'B'
    elif numero <= 30:
        return 'I'
    elif numero <= 45:
        return 'N'
    elif numero <= 60:
        return 'G'
    elif numero <= 75:
        return 'O'

# Configuración de la página de Streamlit
st.title('Simulador de Bingo')

# Usar una variable de sesión para almacenar los números extraídos
if 'numeros_extraidos' not in st.session_state:
    st.session_state['numeros_extraidos'] = set()

# Botón para extraer una nueva balota
if st.button('Extraer Balota'):
    numero, st.session_state['numeros_extraidos'] = generar_numero_aleatorio(1, 75, st.session_state['numeros_extraidos'])
    letra = obtener_letra(numero)
    balota = f"{letra}-{numero}"
    st.success(f"Balota extraída: {balota}")
    texto = f"{letra} {numero}, {letra} {numero}"
    reproducir_voz(texto)

# Mostrar los números que han sido llamados hasta el momento
st.write("Números llamados hasta ahora:")
st.write(sorted(f"{obtener_letra(num)}-{num}" for num in st.session_state['numeros_extraidos']))

# Instrucciones para el usuario
st.write("Haz clic en el botón 'Extraer Balota' para simular la extracción de una nueva balota de bingo.")