import requests

# Configuración de la API
API_KEY = 'sk-543424342'  # Reemplaza con tu API key
API_URL = 'https://api.deepseek.com/v1/chat/completions'  # URL corregida

# Encabezados para la solicitud
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def enviar_mensaje(mensaje):
    # Datos para la solicitud
    data = {
  "model": "deepseek-chat",
  "messages": [
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": mensaje}
  ],
  "temperature": 0.7,
  "max_tokens": 150
}
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as err:
        return f"Error de la API: {err}"
    except Exception as e:
        return f"Error inesperado: {e}"

def main():
    print("Bienvenido al chat bot de DeepSee. Escribe 'salir' para terminar.")

    while True:
        mensaje_usuario = input("Tu: ")
        if mensaje_usuario.lower() == 'salir':
            print("chatbot: ¡Hasta luego!")
            break
        respuesta = enviar_mensaje(mensaje_usuario)
        print(f"chatbot: {respuesta}")

if __name__ == "__main__":
    main()