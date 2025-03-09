"""
Main server file
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import file_uploading, pipeline
from .external_services.patches.custom_docling import export_to_dataframe_new
from app.external_services.patches.custom_docling import TableItem

TableItem.export_to_dataframe = export_to_dataframe_new

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