"""Keys API - 密钥管理接口"""
from fastapi import APIRouter
from services.key_service import KeyService

router = APIRouter(prefix="/api/keys", tags=["keys"])
key_svc = KeyService()

@router.get("")
async def list_keys():
    return key_svc.list_keys()

@router.post("")
async def add_key(key_data: dict):
    return key_svc.add_key(key_data)

@router.delete("/{key_id}")
async def delete_key(key_id: str):
    return key_svc.delete_key(key_id)
