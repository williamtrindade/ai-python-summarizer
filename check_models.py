
import os
import google.generativeai as genai

try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("A variável de ambiente GOOGLE_API_KEY não foi definida.")
    else:
        genai.configure(api_key=api_key)
        print("Modelos de IA generativa disponíveis para sua chave:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
except Exception as e:
    print(f"Ocorreu um erro ao buscar os modelos: {e}")

