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

# Criando uma instância do cliente TikTokLive para a conta "@nananan7081"
client = TikTokLiveClient("@samdraculaxgamer")

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

        if response.status_code == 200:
            print("Dados do top 3 enviados para o Firebase com sucesso!")
        else:
            print("Erro ao enviar dados para o Firebase:", response.status_code)

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

        if response.status_code == 200:
            print("Dados enviados para o Firebase com sucesso!")
        else:
            print("Erro ao enviar dados para o Firebase:", response.status_code)

# Verifica se este arquivo está sendo executado como o principal
if __name__ == '__main__':
    # Executa o cliente e bloqueia a thread principal
    # Utilize 'await client.start()' para execução não bloqueante
    client.run()
