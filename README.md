# Projeto FastAPI com Docker e PostgreSQL

**[Documentação](https://anandacampelo.github.io/API-Nuvem/)**

**[Vídeo de Execução](video_api.webm)**

**[Imagem no Docker Hub](https://hub.docker.com/r/anandajgc/weathercloud)**

## Explicação do Projeto
Este projeto é uma API desenvolvida com FastAPI que realiza operações CRUD e se conecta a um banco de dados PostgreSQL. A aplicação está dockerizada e pode ser executada usando Docker Compose. A API inclui endpoints para registrar usuários, fazer login e consultar previsões do tempo usando a API do OpenWeatherMap.

## Como Executar a Aplicação

**1. Clone o repositório:**
```sh
git clone https://github.com/AnandaCampelo/API-Nuvem.git
cd API-Nuvem
```

**2. Execute a aplicação com Docker Compose:** 
```sh
docker compose up
```

*O arquivo [`compose.yml`](compose.yml) está localizado na raiz do projeto.*

#### Por *Ananda Campelo*