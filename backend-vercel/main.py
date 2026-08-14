from api.v1.blog import router as blog_router
# ==========================================================
# PDF MASTER AI
# Main Application
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles  # <-- TAMBAHAN IMPORT

from api.router import api_router
import models

from middleware.cors import register_cors

# Optional Middleware
# from middleware.logging import register_logging
# from middleware.rate_limit import register_rate_limit

from core.logger import info

# ----------------------------------------------------------
# LOAD ENVIRONMENT
# ----------------------------------------------------------

load_dotenv()

# ----------------------------------------------------------
# APPLICATION LIFESPAN
# ----------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    info("Starting PDF Master AI...")

    yield

    info("Stopping PDF Master AI...")

# ----------------------------------------------------------
# APPLICATION
# ----------------------------------------------------------

app = FastAPI(

    title="PDF Master AI",

    description="Enterprise PDF Processing Platform",

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc",

    openapi_url="/openapi.json",

    lifespan=lifespan

)

# ----------------------------------------------------------
# REGISTER MIDDLEWARE
# ----------------------------------------------------------

register_cors(app)

# Optional
# register_logging(app)
# register_rate_limit(app)

# ----------------------------------------------------------
# MOUNT STATIC FILES (STORAGE) <-- TAMBAHAN DI SINI
# ----------------------------------------------------------

# Pastikan folder 'storage' dibuat jika belum ada
os.makedirs("storage", exist_ok=True)

# Hubungkan URL path '/storage' ke folder fisik 'storage'
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# ----------------------------------------------------------
# REGISTER ROUTER
# ----------------------------------------------------------

app.include_router(

    api_router,

    prefix="/api/v1"

)

# ----------------------------------------------------------
# ROOT
# ----------------------------------------------------------

@app.get(

    "/",

    tags=["Root"]

)
async def root():

    return {

        "application": "PDF Master AI",

        "version": "1.0.0",

        "status": "Running",

        "documentation": "/docs",

        "redoc": "/redoc",

        "api": "/api/v1"

    }

# ----------------------------------------------------------
# HEALTH
# ----------------------------------------------------------

@app.get(

    "/health",

    tags=["Health"]

)
async def health():

    return {

        "success": True,

        "status": "Healthy"

    }

# ----------------------------------------------------------
# GLOBAL EXCEPTION
# ----------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(

    request,

    exc

):

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": str(exc)

        }

    )

# ==========================================================
# END
# ==========================================================
app.include_router(blog_router, prefix="/api/v1")

