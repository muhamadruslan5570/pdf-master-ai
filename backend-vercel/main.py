from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def read_root():
    return {"status": "success", "message": "Backend FastAPI di Vercel Berhasil Aktif!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}