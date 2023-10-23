from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import GiftEvent, CommentEvent
import json
import random
import string
import firebase_admin
from firebase_admin import credentials, db
from RankingPresentes import RankingPresentes

# Inicializa o Firebase Admin SDK com a URL do banco de dados
cred = credentials.Certificate("tikitok-live-firebase-adminsdk-65mg3-95aadfef74.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tikitok-live-default-rtdb.firebaseio.com/'
})


# Criando listas para armazenar informações dos presentes
presentes_unicos = []
presentes_multiplos = [] 


# Função para gerar um ID aleatório com letras e números
def generate_random_id(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        random_id = ''.join(random.choice(characters) for _ in range(length))
        # Verifica se o ID já existe nas listas presentes_unicos e presentes_multiplos
        if random_id not in {key for d in presentes_unicos for key in d.keys()} and \
           random_id not in {key for d in presentes_multiplos for key in d.keys()}:
            return random_id


# Criando uma instância do cliente TikTokLive para a conta "@nananan7081"
client = TikTokLiveClient("@nananan7081")

# Definindo um manipulador de eventos para o evento "gift"


@client.on("gift")
async def on_gift(event: GiftEvent):
    # Presente com sequência e a sequência terminou
    if event.gift.streakable and not event.gift.streaking:
        # print(f"{event.user.unique_id} enviou {event.gift.count}x \"{event.gift.info.name}\"")
        # Gerando um ID aleatório para a chave
        random_id = generate_random_id()
       
        dados_formatados = {
                "img": event.user.avatar.url,
                "presentes": event.gift.count,
                "user": event.user.unique_id,
                "tipo_de_presente": event.gift.info.name,
                "random_id":random_id
            }
        presentes_multiplos.append(dados_formatados)

        ranking = RankingPresentes(presentes_multiplos)
        resultado = ranking.criar_ranking()
        
        if resultado:
            for posicao, (usuario, info) in enumerate(resultado, start=1):
                # Verifique se a posição é 1 e imprima a mensagem correspondente
                if posicao == 1:
                    dados_formatados = {
                        "img": info['foto'],
                        "presentes": info['presentes'],
                        "user": usuario
                    }
                    ref = db.reference('top3')
                    ref.child("top1").set(dados_formatados)
                
                elif posicao == 2:
                    dados_formatados = {
                        "img": info['foto'],
                        "presentes": info['presentes'],
                        "user": usuario
                    }
                    ref = db.reference('top3')
                    ref.child("top2").set(dados_formatados)
                
                elif posicao == 3:
                    dados_formatados = {
                        "img": info['foto'],
                        "presentes": info['presentes'],
                        "user": usuario
                    }
                    ref = db.reference('top3')
                    ref.child("top3").set(dados_formatados)
                
                else:
                    print("A posição não é 1, 2 ou 3.")



                print(f"Posição: {posicao}")
                print(f"Usuário: {usuario}")
                print(f"Foto: {info['foto']}")
                print(f"Número de Presentes: {info['presentes']}")
                print("-" * 30)
            else:
                print("ANALIZANDO")

    
    # Presente sem sequência
    elif not event.gift.streakable:
        # print(f"{event.user.unique_id} enviou \"{event.gift.info.name}\"")
        # Gerando um ID aleatório para a chave
        random_id = generate_random_id()
       
        dados_formatados = {
                "img": event.user.avatar.url,
              "presentes": "1",
                "user": event.user.unique_id,
                "tipo_de_presente": event.gift.info.name,
                "random_id":random_id
            }
        presentes_unicos.append(dados_formatados)
        ref = db.reference('presentes')
        ref.push(dados_formatados)
        print("Dados enviados para o Firebase")

# Verifica se este arquivo está sendo executado como o principal
if __name__ == '__main__':
    # Executa o cliente e bloqueia a thread principal
    # Utilize 'await client.start()' para execução não bloqueante
    client.run()
