"""
Manager API for Qdrant collections
"""
from typing import List, Optional
from fastapi import APIRouter

from models.manager import Manager

router = APIRouter()

@router.delete("/delete")
async def delete_documents(collection_name: str, ids: Optional[List[str]] = None):
    """
    Delete documents from a Qdrant collection by their IDs.
    
    Args:
        collection_name (str): The name of the Qdrant collection to manage.
        ids (Optional[List[str]]): List of document IDs to delete. If None, no documents will be deleted.
        
    Returns:
        dict: A dictionary containing the status of the operation.
    """
    status = Manager(collection_name=collection_name).delete(ids=ids)
    if status:
        return {"status": "success", "message": "Documents deleted successfully"}
    else:
        return {"status": "failed", "message": "Failed to delete documents"}