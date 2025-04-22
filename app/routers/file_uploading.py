"""
File uploading API
"""
from fastapi import APIRouter, File, UploadFile

from models.ingestion import IngestionManager

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), collection_name: str = "tailieu_ftu", header_rows: int = 10):
    """API upload file"""
    status, ids = await IngestionManager(collection_name=collection_name, header_rows=header_rows).ingest(file=file)
    if status:
        return {"status": "success", "ids": ids}
    else:
        return {"status": "failed"}

@router.post("/upload_faq")
async def upload_faq(file: UploadFile = File(...), collection_name: str = "faq", header_rows: int = 10):
    """API upload FAQ file"""
    status, ids = await IngestionManager(collection_name=collection_name, header_rows=header_rows).ingest_faq(file=file)
    if status:
        return {"status": "success", "ids": ids}
    else:
        return {"status": "failed"}