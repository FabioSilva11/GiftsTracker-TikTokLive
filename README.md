## GiftsTracker-TikTokLive – Versão Jogo de Ranking (sem Firebase)

Este projeto é um **tracker de presentes da live do TikTok** que agora funciona como um **jogo de competição de ranking**, totalmente **sem Firebase** e rodando apenas em Python.

Os espectadores mandam presentes na live e o script:
- **Conta automaticamente quantos presentes cada usuário enviou**;
- **Mostra um ranking em tempo real** no terminal (TOP 10);
- **Mostra também a URL da foto (avatar) de cada usuário** em todos os eventos principais;
- Trata automaticamente alguns erros da API do TikTokLive e **tenta reconectar sozinho** quando o problema é externo.

Repositório no GitHub:  
[`https://github.com/FabioSilva11/GiftsTracker-TikTokLive`](https://github.com/FabioSilva11/GiftsTracker-TikTokLive)


## Pré-requisitos

- **Python 3.6 ou superior** (você está usando algo como `C:/Python314/python.exe`, o que é adequado).
- Sistema operacional Windows (testado em Windows 10).  


## Instalação das dependências

No PowerShell (ou terminal), execute usando o mesmo Python que você usa para rodar o script. Exemplo baseado no ambiente atual:

```powershell
C:/Python314/python.exe -m pip install --upgrade TikTokLive
```

Isso instala/atualiza a biblioteca `TikTokLive` usada para conectar na live e receber os eventos (presentes, likes, entradas, etc.).  
**Não é mais necessário instalar `requests` nem configurar Firebase.**


## Configuração

Abra o arquivo `TikTok tracker.py` e ajuste:

- **Conta do TikTok Live a ser monitorada**

```python
client = TikTokLiveClient("@uzzi.pratas.925")
```

Troque `@uzzi.pratas.925` pelo **@ da conta da sua live**, se quiser usar em outra conta.


## Como o jogo de ranking funciona

### 1. Estruturas principais

O script mantém em memória:

- `presentes_unicos` e `presentes_multiplos`: listas com os presentes recebidos (mantidas por compatibilidade com a versão original).
- `ranking_presentes`: dicionário com o **total de presentes por usuário**:
  - Chave: `user_unique_id` (ex.: `@usuario`)
  - Valor: quantidade total de presentes enviados.
- `avatars_usuarios`: dicionário com a **URL do avatar (foto)** de cada usuário.


### 2. Evento de presente (`GiftEvent`)

Para cada presente recebido:

- Se o presente tem sequência e a sequência terminou (`streakable` e não `streaking`):
  - Soma `event.gift.count` para aquele usuário no `ranking_presentes`.
  - Salva os dados em `presentes_multiplos`.
- Se o presente é sem sequência:
  - Soma `1` para aquele usuário no `ranking_presentes`.
  - Salva os dados em `presentes_unicos`.
- Em ambos os casos:
  - Atualiza a URL do avatar do usuário em `avatars_usuarios`.
  - Chama `exibir_ranking()`, que imprime no terminal o **TOP 10** com:
    - `posição, @user, total de presentes, avatar: URL`.


### 3. Outros eventos

Os seguintes eventos também estão tratados e **imprimem mensagens no console com avatar do usuário** quando disponível:

- `LikeEvent` – alguém curtiu a transmissão;
- `JoinEvent` – alguém entrou na live;
- `FollowEvent` – alguém seguiu o streamer;
- `ShareEvent` – alguém compartilhou a live;
- `CommentEvent` – alguém comentou (mostra `nickname`, `@user` e avatar);
- `UserStatsEvent` – atualização de contagem de espectadores (quando disponível);
- `ConnectEvent` / `DisconnectEvent` / `LiveEndEvent` – conexão, desconexão e fim da live.

Em todos os eventos com `event.user`, o script tenta pegar `event.user.avatar.url` (de forma segura) e atualiza o dicionário `avatars_usuarios`. Assim, o ranking sempre tem a foto mais recente conhecida daquele usuário.


## Erros da TikTokLive (SignAPIError) e reconexão automática

Em algumas situações, a biblioteca `TikTokLive` pode falhar ao tentar conectar na live, retornando erro parecido com:

```text
TikTokLive.client.errors.SignAPIError: TikTokLive v6.6.5 -> [SIGN_NOT_200]
Failed request to Sign API with status code 500
{
  "message": "A 504 error occurred whilst fetching the webcast URL.",
  "code": 500
}
```

Esse erro **não é do seu código**, e sim da **Sign API usada internamente pela TikTokLive** (instabilidade, erro 500/504, etc.).  

O script agora trata isso da seguinte forma:

- Envolve `client.run()` em um `while True` com `try/except`.
- Quando ocorre `SignAPIError`:
  - Mostra uma mensagem amigável explicando que é problema externo;
  - **Espera 10 segundos**;
  - **Tenta reconectar automaticamente**.
- Se surgir qualquer outro erro inesperado (`Exception` genérica):
  - Mostra o erro no console;
  - Encerra para você poder ver o problema.


## Como executar

1. Garanta que está na pasta correta:

   ```powershell
   cd C:\Users\produ\Desktop\GiftsTracker-TikTokLive
   ```

2. Execute o script com o Python correto (ajuste se precisar):

   ```powershell
   C:/Python314/python.exe "TikTok tracker.py"
   ```

3. Inicie a live na conta configurada em `TikTokLiveClient("@seu_usuario")`.
4. Conforme as pessoas entrarem, curtirem, seguirem, compartilharem, comentarem e mandarem presentes, você verá no terminal:
   - Mensagens de cada evento com `@user` e **URL do avatar**;
   - O **ranking atualizado de presentes** mostrando TOP 10.


## Diferenças em relação à versão original (Firebase)

Comparando com a versão original deste repositório descrita no README antigo em [`GiftsTracker-TikTokLive`](https://github.com/FabioSilva11/GiftsTracker-TikTokLive):

- **Removido**: uso de Firebase (nenhuma chamada HTTP para banco de dados em tempo real).
- **Mantido**: estrutura básica de captura de presentes (`presentes_unicos`, `presentes_multiplos`).
- **Adicionado**:
  - Jogo de **ranking de presentes** em memória.
  - Impressão de **URL dos avatares** dos usuários em todos os eventos principais.
  - Tratamento de `SignAPIError` com **reconexão automática**.

Se você quiser, pode futuramente integrar esse ranking e os avatares em um **overlay para OBS** (por exemplo, uma página HTML que lê um arquivo JSON gerado pelo script). Essa parte não está implementada ainda, mas o código atual já fornece todas as informações necessárias.


## Publicação no GitHub

Este projeto está publicado em:  
[`https://github.com/FabioSilva11/GiftsTracker-TikTokLive`](https://github.com/FabioSilva11/GiftsTracker-TikTokLive)

Para atualizar o repositório com novas mudanças (por exemplo, após editar o script ou este README), use:

```powershell
cd C:\Users\produ\Desktop\GiftsTracker-TikTokLive
git status
git add "TikTok tracker.py" README.md
git commit -m "Atualiza para jogo de ranking sem Firebase e adiciona README detalhado"
git push origin main
```


## Suporte

Para suporte ou dúvidas sobre o projeto, utilize o e-mail já informado no repositório original:  
**produtorfabiosilva@gmail.com**.


