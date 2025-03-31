import requests

# Configuración de la API
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e'  # Reemplaza con tu API key
API_URL = 'https://api.deepseek.com/v1/chat/completions'

# Encabezados para la solicitud
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def analizar_sentimiento(mensaje):
    """
    Envía un mensaje a la API y analiza el sentimiento.
    Retorna 'Positivo', 'Negativo' o 'Neutral' basado en la respuesta.
    """
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres un asistente de análisis de sentimientos. Devuelve si el sentimiento del texto es 'Positivo', 'Negativo' o 'Neutral'."},
            {"role": "user", "content": f"Analiza el sentimiento del siguiente texto: {mensaje}"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        respuesta = response.json()['choices'][0]['message']['content'].strip()

        # Normalizamos la respuesta para asegurar que sea uno de los tres sentimientos
        if "positivo" in respuesta.lower():
            return "Positivo 😊"
        elif "negativo" in respuesta.lower():
            return "Negativo 😡"
        else:
            return "Neutral 😐"
    
    except requests.exceptions.HTTPError as err:
        return f"Error de la API: {err}"
    except Exception as e:
        return f"Error inesperado: {e}"

def main():
    print("Bienvenido al Analizador de Sentimientos 🎭. Escribe 'salir' para terminar.")

    while True:
        mensaje_usuario = input("\n💬 Escribe un comentario: ")
        if mensaje_usuario.lower() == 'salir':
            print("👋 ¡Hasta luego!")
            break
        sentimiento = analizar_sentimiento(mensaje_usuario)
        print(f"🧐 Análisis de Sentimiento: {sentimiento}")

if __name__ == "__main__":
    main()
