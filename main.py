import google.generativeai as generai
import os

from dotenv import load_dotenv

load_dotenv()
generai.configure(api_key=os.getenv("API_KEY_GEMINI"))

# listar os modelos que interessa
for modelo in generai.list_models():
  if 'generateContent' in modelo.supported_generation_methods:
    print("_____________________________")
    print("# " + modelo.name)
    print(modelo.display_name)
    print(modelo.description)

# Escolher o modelo
model = generai.GenerativeModel("gemini-1.5-pro-latest")

# Testando o Modelo
response = model.generate_content("Essa é uma mensagem de teste. O que você é capaz de fazer?")
print(response.text)

# Criando o chatbot
chat = model.start_chat(history=[])
prompt = input("Digite uma pergunta: ")
while prompt != "fim":
  response = chat.send_message(prompt)
  print(response.text)
  prompt = input("Digite uma pergunta: ")



