"""
File uploading API
"""
from fastapi import APIRouter, File, UploadFile

from models.ingestion import IngestionManager

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), collection_name: str = "tailieu_ftu"):
    """API upload file"""
    status = await IngestionManager(collection_name=collection_name).ingest(file=file)
    if status:
        return {"status": "success"}

@router.post("/upload_faq")
async def upload_faq(file: UploadFile = File(...), collection_name: str = "faq"):
    """API upload FAQ file"""
    status = await IngestionManager(collection_name=collection_name).ingest_faq(file=file)
    if status:
        return {"status": "success"}