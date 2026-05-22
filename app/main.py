from fastapi import FastAPI
from app.routes import tmdb, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tmdb.router)
app.include_router(auth.router)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}