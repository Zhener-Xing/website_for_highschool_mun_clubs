from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import captcha, teams, payments, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NOVA Team Registration API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(captcha.router)
app.include_router(teams.router)
app.include_router(payments.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="app/assets"), name="static")


@app.get("/")
def root():
    return {"status": "ok"}
