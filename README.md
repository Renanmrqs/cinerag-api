# CineRAG Analytics — API

API REST + WebSocket de uma plataforma de análise de sentimentos de filmes com assistente de IA integrado. Consome a API do TMDB para busca de filmes, usa um modelo próprio de ML ([SentimentAI](https://github.com/Renanmrqs/SentimentAI)) para análise de reviews e integra o Google Gemini para o chat CineAI.

🔗 **[Frontend](https://cinerag-analytics.vercel.app)** · **[Repositório Frontend](https://github.com/Renanmrqs/cinerag-frontend)**

---

## Funcionalidades

- Autenticação JWT com blacklist de tokens para logout seguro
- Login social via Google OAuth2 com fluxo de completar perfil
- Busca de filmes via TMDB, filtrada para retornar apenas filmes com reviews disponíveis
- Análise de sentimento (positive / negative / mixed) com score de confiança — powered by SentimentAI
- Cache de análises no banco para evitar chamadas repetidas ao modelo
- Favoritos por usuário com constraint de unicidade no banco
- Chat em tempo real via WebSocket com autenticação por token no query param
- Queries fixas sobre os favoritos do usuário (`/positives`, `/negatives`, `/most trusted`, etc.)
- Assistente CineAI via Google Gemini — responde perguntas abertas com contexto dos favoritos do usuário e histórico da conversa

---

## Stack

| | |
|---|---|
| **Python + FastAPI** | Framework principal e WebSocket |
| **PostgreSQL (Neon)** | Banco de dados em produção |
| **SQLAlchemy + Alembic** | ORM e migrations versionadas |
| **PyJWT + Argon2** | Autenticação e hash de senhas |
| **Authlib** | Google OAuth2 |
| **Google Gemini** | Modelo de linguagem para o CineAI |
| **TMDB API** | Dados de filmes e reviews |
| **SentimentAI** | Modelo próprio de ML para análise de sentimento |
| **Pytest + GitHub Actions** | Testes automatizados a cada push |
| **Docker** | Containerização da aplicação |

---

## Arquitetura

```
app/
├── routes/          # Endpoints HTTP (auth, filmes, favoritos)
├── services/        # Lógica de negócio separada das rotas
├── ws/
│   ├── manager.py   # Gerencia conexões ativas por username
│   └── websocket.py # Endpoint WS — queries fixas + Gemini fallback
├── models.py        # Models SQLAlchemy
├── schemas.py       # Schemas Pydantic
├── auth.py          # JWT — geração e verificação de tokens
└── database.py      # Engine e sessão do banco
alembic/             # Migrations versionadas
```

---

## Como rodar localmente

**Pré-requisitos:** Python 3.12+, PostgreSQL (ou conta no Neon), chaves de API do TMDB, Google OAuth2 e Google Gemini.

```bash
git clone https://github.com/Renanmrqs/cinerag-api.git
cd cinerag-api

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# preencha o .env com suas credenciais

alembic upgrade head

uvicorn app.main:app --reload
```

### Variáveis de ambiente

```env
DATABASE_URL=
SECRET_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GEMINI_API_KEY=
```

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Registro de usuário |
| POST | `/auth/login` | Login — retorna JWT |
| POST | `/auth/logout` | Logout — invalida o token |
| GET | `/auth/google` | Inicia fluxo OAuth2 Google |
| PATCH | `/auth/complete-profile` | Completa perfil de usuário Google |
| GET | `/films/search_film/{name}` | Busca filmes no TMDB |
| GET | `/films/get_score/{id}` | Análise de sentimento do filme |
| POST | `/films/favorites/post_film` | Adiciona filme aos favoritos |
| GET | `/films/favorites/get_all` | Lista favoritos do usuário |
| DELETE | `/films/favorites/del_fav` | Remove favorito |
| WS | `/ws?token=` | Chat CineAI em tempo real |

Documentação interativa em `/docs`.

---

## Comandos do CineAI

| Comando | Descrição |
|---------|-----------|
| `/positives` | Filmes positivos nos favoritos |
| `/negatives` | Filmes negativos nos favoritos |
| `/mixeds` | Filmes mistos nos favoritos |
| `/most trusted` | Filme com maior confiança |
| `/smaller trusted` | Filme com menor confiança |
| `/count films` | Total de favoritos |
| `/first film added` | Primeiro favorito adicionado |
| `/last film added` | Último favorito adicionado |
| Qualquer outra mensagem | Respondido pelo Gemini com contexto dos favoritos |

---

## Projetos relacionados

- [SentimentAI](https://github.com/Renanmrqs/SentimentAI) — modelo de ML próprio consumido por esta API
- [CineRAG Frontend](https://github.com/Renanmrqs/cinerag-frontend) — interface em HTML/CSS/JS vanilla

---

## Autor

**Renan Fernandes Marques** — [LinkedIn](https://linkedin.com/in/renan-marques-dev-python) · [GitHub](https://github.com/Renanmrqs)