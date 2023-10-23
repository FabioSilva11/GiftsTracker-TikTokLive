# GiftsTracker-TikTokLive

## Introdução

Este script Python foi desenvolvido como parte de um projeto de transmissão ao vivo interativa, que se integra com um aplicativo. Ele é usado para capturar e gerenciar eventos de presentes durante uma transmissão ao vivo no TikTokLive. Este script é uma parte de um sistema maior que inclui um aplicativo correspondente. Para obter suporte ou discutir o projeto, entre em contato com o desenvolvedor em **produtorfabiosilva@gmail.com**.

## Vídeo Demonstrativo

Assista a uma demonstração de uso desse projeto no vídeo abaixo:

<video width="320" height="240" controls>
  <source src="Screenrecorder-2023-10-23-03-01-57-868.mp4" type="video/mp4">
  Seu navegador não suporta o elemento de vídeo.
</video>


## Pré-requisitos

- **Python 3.6 ou superior**
- **Banco de dados do Firebase:** O script está integrado com o Firebase para armazenamento em tempo real dos dados dos presentes.

## Instalação

Antes de executar o script, você precisa instalar as dependências. No terminal, use o seguinte comando para instalar as bibliotecas necessárias:

```bash
pip install TikTokLive requests
```

## Configuração

Antes de executar o script, você precisa configurar algumas variáveis no código:

- `firebase_url`: Atualize esta variável com a URL do seu banco de dados em tempo real do Firebase.
- `client = TikTokLiveClient("@seu_usuario_do_tiktoklive")`: Substitua `"@seu_usuario_do_tiktoklive"` pelo seu nome de usuário no TikTokLive.

## Funcionalidades

### Presentes Únicos

- Quando um presente não streakable é enviado durante a transmissão, os dados do presente são formatados e enviados diretamente para o Firebase usando uma chamada HTTP POST.
- Cada presente único é registrado com informações sobre o usuário que enviou o presente, a imagem do usuário, o tipo de presente e um ID único gerado aleatoriamente.

### Presentes Streakable (Múltiplos)

- Quando um presente streakable (múltiplos) é enviado durante a transmissão, os dados do presente são formatados e classificados com base no número de presentes enviados pelo usuário.
- Os três principais presentadores (usuários que enviaram o maior número de presentes) são identificados e suas informações são enviadas para o Firebase usando uma chamada HTTP PUT para atualizar a lista `top3`.
- A lista `top3` no Firebase contém informações sobre os três principais presentadores, incluindo a imagem do usuário, o número de presentes enviados e o nome de usuário.

## Execução

Para executar o script, use o seguinte comando no terminal:

```bash
python nome_do_script.py
```

Certifique-se de que seu ambiente Python tenha as permissões necessárias para acessar o TikTokLive e o Firebase. O script começará a capturar eventos de presentes assim que for executado.

## Observações

- **Segurança:** Este script lida com informações do usuário e deve ser usado com cuidado. Certifique-se de proteger suas credenciais e os dados do Firebase.
- **Personalização:** Este é um exemplo básico. Como parte de um projeto maior, você pode personalizar o script para incluir mais funcionalidades ou para lidar com outros tipos de eventos do TikTokLive, se necessário.

## Suporte

Para obter suporte ou discutir o projeto, entre em contato com o desenvolvedor em **produtorfabiosilva@gmail.com**.

---

Este README detalhado fornece informações abrangentes sobre a configuração, o uso e as funcionalidades do script. Certifique-se de entender completamente o código e as implicações de segurança antes de executá-lo em um ambiente de produção. Para desenvolver seu próprio projeto, você pode usar este script como um ponto de partida e personalizá-lo de acordo com suas necessidades.
