from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    GiftEvent,
    ConnectEvent,
    DisconnectEvent,
    LikeEvent,
    JoinEvent,
    FollowEvent,
    ShareEvent,
    CommentEvent,
    UserStatsEvent,
    LiveEndEvent,
)
from TikTokLive.client.errors import SignAPIError
import random
import string

# Criando listas para armazenar informações dos presentes
presentes_unicos = []
presentes_multiplos = []

# Dicionário para armazenar a pontuação (quantidade de presentes) por usuário
ranking_presentes = {}  # { "user_unique_id": total_de_presentes }

# Dicionário para armazenar o avatar (foto) de cada usuário
avatars_usuarios = {}  # { "user_unique_id": "url_do_avatar" }


# Função para gerar um ID aleatório com letras e números
def generate_random_id(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        random_id = "".join(random.choice(characters) for _ in range(length))
        # Verifica se o ID já existe nas listas presentes_unicos e presentes_multiplos
        if random_id not in {d["random_id"] for d in presentes_unicos} and \
           random_id not in {d["random_id"] for d in presentes_multiplos}:
            return random_id


def atualizar_ranking(user_id: str, quantidade: int):
    """
    Atualiza o ranking de presentes para o usuário.
    """
    if user_id not in ranking_presentes:
        ranking_presentes[user_id] = 0
    ranking_presentes[user_id] += quantidade


def exibir_ranking(top_n: int = 10):
    """
    Mostra no console o ranking dos usuários com mais presentes.
    """
    if not ranking_presentes:
        return

    ranking_ordenado = sorted(
        ranking_presentes.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    print("\n===== RANKING DE PRESENTES =====")
    for posicao, (user_id, total) in enumerate(ranking_ordenado, start=1):
        avatar = avatars_usuarios.get(user_id, "sem avatar conhecido")
        print(f"{posicao}º - @{user_id}: {total} presentes | avatar: {avatar}")
    print("================================\n")


# Criando uma instância do cliente TikTokLive para a conta
client = TikTokLiveClient("@uzzi.pratas.925")

# Definindo um manipulador de eventos para o evento "gift"
@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    # Presente com sequência e a sequência terminou
    if event.gift.streakable and not event.gift.streaking:
        quantidade_presentes = event.gift.count
        random_id = generate_random_id()
        dados_formatados = {
            "img": event.user.avatar.url,
            "presentes": quantidade_presentes,
            "user": event.user.unique_id,
            "tipo_de_presente": event.gift.info.name,
            "random_id": random_id
        }
        presentes_multiplos.append(dados_formatados)

        # Atualiza avatar conhecido desse usuário
        avatars_usuarios[event.user.unique_id] = event.user.avatar.url

        # Atualiza ranking do jogo
        atualizar_ranking(event.user.unique_id, quantidade_presentes)

    # Presente sem sequência
    elif not event.gift.streakable:
        quantidade_presentes = 1
        random_id = generate_random_id()
        dados_formatados = {
            "img": event.user.avatar.url,
            "presentes": quantidade_presentes,
            "user": event.user.unique_id,
            "tipo_de_presente": event.gift.info.name,
            "random_id": random_id
        }
        presentes_unicos.append(dados_formatados)

        # Atualiza avatar conhecido desse usuário
        avatars_usuarios[event.user.unique_id] = event.user.avatar.url

        # Atualiza ranking do jogo
        atualizar_ranking(event.user.unique_id, quantidade_presentes)

    # Exibe sempre o ranking após um presente
    exibir_ranking()

# Manipulador de eventos para quando a conexão é estabelecida
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print("Conectado à transmissão ao vivo.")


# Manipulador de eventos para quando a conexão é encerrada
@client.on(DisconnectEvent)
async def on_disconnect(event: DisconnectEvent):
    print("Desconectado da transmissão ao vivo.")


# Manipulador de eventos para quando alguém curte a transmissão
@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    avatar = getattr(event.user, "avatar", None)
    avatar_url = getattr(avatar, "url", "sem avatar conhecido") if avatar is not None else "sem avatar conhecido"
    # Atualiza avatar conhecido desse usuário
    avatars_usuarios[event.user.unique_id] = avatar_url

    print(f"@{event.user.unique_id} curtiu a transmissão! | avatar: {avatar_url}")


# Manipulador de eventos para quando alguém entra na transmissão
@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    avatar = getattr(event.user, "avatar", None)
    avatar_url = getattr(avatar, "url", "sem avatar conhecido") if avatar is not None else "sem avatar conhecido"
    avatars_usuarios[event.user.unique_id] = avatar_url

    print(f"@{event.user.unique_id} entrou na transmissão! | avatar: {avatar_url}")


# Manipulador de eventos para quando alguém segue o streamer
@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    avatar = getattr(event.user, "avatar", None)
    avatar_url = getattr(avatar, "url", "sem avatar conhecido") if avatar is not None else "sem avatar conhecido"
    avatars_usuarios[event.user.unique_id] = avatar_url

    print(f"@{event.user.unique_id} seguiu o streamer! | avatar: {avatar_url}")


# Manipulador de eventos para quando alguém compartilha a transmissão
@client.on(ShareEvent)
async def on_share(event: ShareEvent):
    avatar = getattr(event.user, "avatar", None)
    avatar_url = getattr(avatar, "url", "sem avatar conhecido") if avatar is not None else "sem avatar conhecido"
    avatars_usuarios[event.user.unique_id] = avatar_url

    print(f"@{event.user.unique_id} compartilhou a transmissão! | avatar: {avatar_url}")


# Manipulador de eventos para quando alguém comenta na transmissão
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    avatar = getattr(event.user, "avatar", None)
    avatar_url = getattr(avatar, "url", "sem avatar conhecido") if avatar is not None else "sem avatar conhecido"
    avatars_usuarios[event.user.unique_id] = avatar_url

    print(f"{event.user.nickname} (@{event.user.unique_id}) | avatar: {avatar_url} -> {event.comment}")


# Manipulador de eventos para quando a contagem de espectadores é atualizada
@client.on(UserStatsEvent)
async def on_viewer_update(event: UserStatsEvent):
    # Nem sempre a estrutura é a mesma, então mostramos o objeto inteiro se não houver atributo específico
    viewer_count = getattr(event, "total_viewers", None) or getattr(event, "viewer_count", None)
    if viewer_count is not None:
        print("Nova contagem de espectadores:", viewer_count)
    else:
        print("Atualização de estatísticas de usuário recebida:", event)


# Manipulador de eventos para quando a transmissão ao vivo é encerrada pelo host
@client.on(LiveEndEvent)
async def on_live_end(event: LiveEndEvent):
    print("A transmissão ao vivo foi encerrada pelo host.")


# Verifica se este arquivo está sendo executado como o principal
if __name__ == "__main__":
    # Tenta executar o cliente em loop, tratando erros da Sign API
    while True:
        try:
            # Executa o cliente e bloqueia a thread principal
            # Utilize 'await client.start()' para execução não bloqueante
            client.run()
            break  # Se sair normalmente, não precisa tentar de novo
        except SignAPIError as e:
            # Erro da API de assinatura do TikTokLive (problema externo, não do código)
            print("\n[AVISO] Erro ao conectar na live (SignAPIError).")
            print("Detalhes:", e)
            print("Isso geralmente é um problema temporário do servidor de assinatura ou da conexão.\n"
                  "O script vai tentar reconectar em alguns segundos...\n")

            import time
            time.sleep(10)
        except Exception as e:
            # Qualquer outro erro inesperado: mostramos e encerramos para você ver o problema
            print("\n[ERRO] Erro inesperado ao executar o cliente TikTokLive:")
            print(e)
            break
