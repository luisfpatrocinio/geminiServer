import google.generativeai as generai
import os
import websockets
import asyncio
import json

from config import MODEL_NAME, MODEL_PROMPT

from dotenv import load_dotenv
load_dotenv()
generai.configure(api_key=os.getenv("API_KEY_GEMINI"))

# Escolher o modelo
# model = generai.GenerativeModel("gemini-1.5-pro-latest")
model = generai.GenerativeModel(MODEL_NAME)



# Testando o Modelo
# response = model.generate_content("Essa é uma mensagem de teste. O que você é capaz de fazer?")
# print(response.text)

# Lista de clientes conectados e contagem de jogadores:
connected_clients = set()

async def sendMessage(message):
    for conn in connected_clients:
        await conn.send(json.dumps(
            {
                "type": "ai_response", 
                "content": message
            }
        ))

async def server(ws, path):

    # Para fins de testes, listar modelos de linguagem.
    # listar os modelos que interessa
    # for modelo in generai.list_models():
    #   if 'generateContent' in modelo.supported_generation_methods:
    #     print("_____________________________")
    #     print("# " + modelo.name)
    #     print(modelo.display_name)
    #     print(modelo.description)

    # Registrar cliente:
    connected_clients.add(ws)
    print(f"Novo Cliente Conectado: {ws.remote_address}")

    # Inicializando o chat
    chat = model.start_chat(history=[{"role": "model", "parts": MODEL_PROMPT}])
    print("Chat iniciado: ", chat)

    # Mensagem de boas vindas
    response = chat.send_message("Sua primeira mensagem será sua apresentação: Se apresente.")
    _startMessage = response.text
    await sendMessage(_startMessage)

    try:
        async for msg in ws:
            message = json.loads(msg)
            print("Mensagem recebida: ", message)
            if message['type'] == 'user_message':
                # Mandar a mensagem para o chat
                for conn in connected_clients:
                    # await conn.send(json.dumps(
                    #     {
                    #         "type": "ai_response", 
                    #         "content": "processando sua msg"
                    #     }
                    # ))
                    response = chat.send_message(message['content'])
                    msgToSend = response.text
                    await sendMessage(msgToSend)
                    print("Resposta do chat: ", msgToSend)


    except Exception as e:
        print(f"Erro na conexão com {ws.remote_address}: \n{e}")
    finally:
        if ws in connected_clients:
            connected_clients.remove(ws)
            print(f"Cliente Desconectado: {ws.remote_address}")
            

def main():
    start_server = websockets.serve(server, "0.0.0.0", 10000)
    # start_server = websockets.serve(server, "localhost", 10000)    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    print("Servidor iniciado.")
    loop.run_forever()

if __name__ == "__main__":
    main()
