import os
from dotenv import load_dotenv
from google import genai

# 1. Cargamos el .env manualmente
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Inicializamos el cliente
client = genai.Client(api_key=api_key)

print("Conectando a Google para ver los modelos permitidos...\n")

try:
    # 3. Llamamos al método list() del nuevo SDK
    model_list = client.models.list()
    
    print("✅ Modelos disponibles para esta API Key:")
    print("-" * 40)
    for model in model_list:
        # Imprimimos el nombre del modelo
        print(f"- {model.name}")
        
except Exception as e:
    print(f"❌ Error al obtener la lista: {e}")