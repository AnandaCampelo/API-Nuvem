# Projeto FastAPI com Docker e PostgreSQL

**[Documentação](https://anandacampelo.github.io/API-Nuvem/)**

**[Vídeo de funcionamento local](https://anandacampelo.github.io/API-Nuvem/video_exemplo.webm)**

**[API pela AWS]([docs/video_exemplo.webm](http://aabf021d170204a16a8ff69c689a1cf9-1954537924.us-east-1.elb.amazonaws.com/docs#/))**

**[Imagem no Docker Hub](https://hub.docker.com/r/anandajgc/weathercloud)**

#### Por *Ananda Campelo*

## Explicação do Projeto
Este projeto é uma API desenvolvida com FastAPI que realiza operações CRUD e se conecta a um banco de dados PostgreSQL. A aplicação está dockerizada e pode ser executada usando Docker Compose. A API inclui endpoints para registrar usuários, fazer login e consultar previsões do tempo usando a API do OpenWeatherMap.

## Como Executar a Aplicação

**1. Clone o repositório:**
```sh
git clone https://github.com/AnandaCampelo/API-Nuvem.git
cd API-Nuvem
```

**2. Execute a aplicação com Docker Compose:** [^1]
```sh
docker compose up -d
```

[^1]: *O arquivo [`compose.yml`](compose.yml) está localizado na raiz do projeto.*
