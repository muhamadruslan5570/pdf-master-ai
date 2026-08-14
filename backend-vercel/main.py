from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="PDF Master AI - Vercel API")

origins = [
    "https://pdf-master-ai.muhamadruslan5570.workers.dev",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginSchema(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "Backend FastAPI di Vercel Berhasil Aktif!"}

@app.post("/login")
@app.post("/api/login")
def login(data: LoginSchema):
    # Endpoint dummy untuk verifikasi koneksi frontend-backend
    return {
        "status": "success",
        "message": "Login berhasil!",
        "access_token": "dummy-token-vercel-12345",
        "user": {"email": data.email or data.username, "name": "User Master"}
    }