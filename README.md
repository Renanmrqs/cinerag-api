# CineRAG Analytics — API

API REST + WebSocket de uma plataforma de análise de sentimentos de filmes com assistente de IA integrado. O projeto consome a API do TMDB para busca de filmes, utiliza um modelo próprio de ML ([SentimentAI](https://github.com/Renanmrqs/SentimentAI)) para análise de reviews e integra o Google Gemini para o chat inteligente CineAI.

---

## Funcionalidades

- Autenticação JWT com blacklist de tokens (logout seguro)
- Login social via Google OAuth2
- Busca de filmes via TMDB com filtro de filmes sem reviews
- Análise de sentimento por filme (positive / negative / mixed) com score de confiança — powered by SentimentAI
- Cache de análises no banco para evitar chamadas repetidas
- Favoritos por usuário com constraint de unicidade
- Chat em tempo real via WebSocket com autenticação por token
- Queries fixas sobre os favoritos do usuário (`/positives`, `/negatives`, `/most trusted`, etc.)
- Assistente CineAI com Google Gemini — responde perguntas abertas com contexto dos filmes favoritos do usuário
- Histórico de chat salvo no banco com persistência de contexto

---

## Stack

- **Python** — linguagem principal
- **FastAPI** — framework web e WebSocket
- **PostgreSQL** (Neon) — banco de dados
- **SQLAlchemy** — ORM
- **Alembic** — migrations versionadas
- **PyJWT + Argon2** — autenticação e hash de senhas
- **Pytest** - Testes integrados no GitHub
- **Authlib** — Google OAuth2
- **Google Gemini** — modelo de linguagem para o CineAI
- **TMDB API** — dados de filmes e reviews
- **SentimentAI** — modelo próprio de análise de sentimento (deploy no Render)


---

## Arquitetura

```
app/
├── routes/         # Endpoints HTTP (auth, filmes, favoritos)
├── services/       # Lógica de negócio separada das rotas
├── ws/             # WebSocket — manager de conexões e endpoint
│   ├── manager.py  # Gerencia conexões ativas por username
│   └── websocket.py# Endpoint WS com queries fixas + Gemini fallback
├── models.py       # Models SQLAlchemy
├── schemas.py      # Schemas Pydantic
├── auth.py         # JWT — geração e verificação de tokens
└── database.py     # Engine e sessão do banco
alembic/            # Migrations versionadas
```

---

## Como rodar localmente

### Pré-requisitos

- Python 3.12+
- PostgreSQL (ou conta no Neon)
- Chaves de API: TMDB, Google OAuth2, Google Gemini

### Passo a passo

```bash
# Clone o repositório
git clone https://github.com/Renanmrqs/cinerag-api.git
cd cinerag-api

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Rode as migrations
alembic upgrade head

# Inicie o servidor
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

## Endpoints principais

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Registro de usuário |
| POST | `/auth/login` | Login — retorna JWT |
| POST | `/auth/logout` | Logout — adiciona token à blacklist |
| GET | `/auth/google` | Inicia fluxo OAuth2 Google |
| GET | `/films/search_film/{name}` | Busca filmes no TMDB |
| GET | `/films/get_score/{id}` | Análise de sentimento do filme |
| POST | `/films/favorites/post_film` | Adiciona filme aos favoritos |
| GET | `/films/favorites/get_all` | Lista favoritos do usuário |
| DELETE | `/films/favorites/del_fav` | Remove favorito |
| WS | `/ws?token=` | Chat CineAI em tempo real |

Documentação interativa disponível em `/docs` (Swagger).

---

## Chat CineAI — Comandos

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
- [CineRAG Frontend](https://github.com/Renanmrqs/cinerag-frontend) — interface web em HTML/CSS/JS vanilla

---

## Autor

**Renan Fernandes Marques**

[LinkedIn](https://linkedin.com/in/renan-marques-dev-python) · [GitHub](https://github.com/Renanmrqs)