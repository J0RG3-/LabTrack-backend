from fastapi import APIRouter, HTTPException
from src.services.supabase_client import supabase

router = APIRouter()

@router.get("/", summary="Listar todos los compuestos")
def list_compounds():
    response = supabase.table("compounds").select("*").execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    return response.data


@router.get("/{compound_id}", summary="Obtener un compuesto por ID")
def get_compound(compound_id: str):
    response = supabase.table("compounds").select("*").eq("id", compound_id).single().execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    if not response.data:
        raise HTTPException(status_code=404, detail="Compuesto no encontrado")
    return response.data


@router.post("/", summary="Crear un nuevo compuesto")
def create_compound(compound: dict):
    response = supabase.table("compounds").insert(compound).execute()
    if response.error:
        raise HTTPException(status_code=500, detail=response.error.message)
    return response.data
