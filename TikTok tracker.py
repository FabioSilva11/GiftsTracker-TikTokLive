from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import GiftEvent
import random
import string
import requests

# Criando listas para armazenar informações dos presentes
presentes_unicos = []
presentes_multiplos = []

# URL do seu banco de dados em tempo real do Firebase
firebase_url = "https://tikitok-live-default-rtdb.firebaseio.com/"

# Função para gerar um ID aleatório com letras e números
def generate_random_id(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        random_id = ''.join(random.choice(characters) for _ in range(length))
        # Verifica se o ID já existe nas listas presentes_unicos e presentes_multiplos
        if random_id not in {d['random_id'] for d in presentes_unicos} and \
           random_id not in {d['random_id'] for d in presentes_multiplos}:
            return random_id

# Criando uma instância do cliente TikTokLive para a conta, exemplo "@samdraculaxgamer"
client = TikTokLiveClient("@sleepstreamxxx")

# Definindo um manipulador de eventos para o evento "gift"
@client.on("gift")
async def on_gift(event: GiftEvent):
    # Presente com sequência e a sequência terminou
    if event.gift.streakable and not event.gift.streaking:
        random_id = generate_random_id()
        dados_formatados = {
            "img": event.user.avatar.url,
            "presentes": event.gift.count,
            "user": event.user.unique_id,
            "tipo_de_presente": event.gift.info.name,
            "random_id": random_id
        }
        presentes_multiplos.append(dados_formatados)

        # Classificar e criar ranking
        ranking = sorted(presentes_multiplos, key=lambda x: x['presentes'], reverse=True)[:3]

        # Enviar dados classificados para o Firebase usando chamadas HTTP POST
        top3_data = []
        for posicao, info in enumerate(ranking, start=1):
            dados_formatados = {
                "img": info['img'],
                "presentes": info['presentes'],
                "user": info['user']
            }
            top3_data.append(dados_formatados)

        # Enviar dados para o Firebase usando chamada HTTP PUT para atualizar a lista top3
        firebase_endpoint = firebase_url + "top3.json"
        response = requests.put(firebase_endpoint, json=top3_data)

    # Presente sem sequência
    elif not event.gift.streakable:
        random_id = generate_random_id()
        dados_formatados = {
            "img": event.user.avatar.url,
            "presentes": 1,
            "user": event.user.unique_id,
            "tipo_de_presente": event.gift.info.name,
            "random_id": random_id
        }
        presentes_unicos.append(dados_formatados)

        # Enviar dados para o Firebase usando chamada HTTP POST
        firebase_endpoint = firebase_url + "presentes.json"
        response = requests.post(firebase_endpoint, json=dados_formatados)

# Manipulador de eventos para quando a conexão é estabelecida
@client.on("connect")
async def on_connect(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": "Conectado à transmissão ao vivo."
    }
    print("Conectado à transmissão ao vivo.")


    firebase_endpoint = firebase_url + "status/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando a conexão é encerrada
@client.on("disconnect")
async def on_disconnect(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": "Desconectado da transmissão ao vivo."
    }
    print("Desconectado da transmissão ao vivo.")
    # Envia os dados para o Firebase

    firebase_endpoint = firebase_url + "status/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando alguém curte a transmissão
@client.on("like")
async def on_like(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": f"@{event.user.unique_id} curtiu a transmissão!"
    }
    print(f"@{event.user.unique_id} curtiu a transmissão!")
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "curtidas/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando alguém entra na transmissão
@client.on("join")
async def on_join(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": f"@{event.user.unique_id} entrou na transmissão!"
    }
    print(f"@{event.user.unique_id} entrou na transmissão!")
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "entradas/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando alguém segue o streamer
@client.on("follow")
async def on_follow(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": f"@{event.user.unique_id} seguiu o streamer!"
    }
    print(f"@{event.user.unique_id} seguiu o streamer!")
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "seguidores/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando alguém compartilha a transmissão
@client.on("share")
async def on_share(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": f"@{event.user.unique_id} compartilhou a transmissão!"
    }
    print(f"@{event.user.unique_id} compartilhou a transmissão!")
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "compartilhamentos/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando alguém comenta na transmissão
@client.on("comment")
async def on_comment(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": f"{event.user.nickname} -> {event.comment}"
    }
    print(f"{event.user.nickname} -> {event.comment}")
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "comentarios/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando a contagem de espectadores é atualizada
@client.on("viewer_update")
async def on_viewer_update(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": "Nova contagem de espectadores:" + str(event.viewer_count)
    }
    print("Nova contagem de espectadores:", event.viewer_count)
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "espectadores/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Manipulador de eventos para quando a transmissão ao vivo é encerrada pelo host
@client.on("live_end")
async def on_live_end(event):
    # Dados que você deseja enviar para o Firebase
    data = {
        "pronpt": "A transmissão ao vivo foi encerrada pelo host."
    }
    print("A transmissão ao vivo foi encerrada pelo host.")
    # Envia os dados para o Firebase
    firebase_endpoint = firebase_url + "status/status.json"
    response = requests.put(firebase_endpoint, json=data)

# Verifica se este arquivo está sendo executado como o principal
if __name__ == '__main__':
    # Executa o cliente e bloqueia a thread principal
    # Utilize 'await client.start()' para execução não bloqueante
    client.run()
