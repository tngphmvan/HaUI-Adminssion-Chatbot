"""
Main server file
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import file_uploading, pipeline, manager

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(file_uploading.router)

app.include_router(pipeline.router)

app.include_router(manager.router)
