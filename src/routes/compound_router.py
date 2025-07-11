from os import stat
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.models.compound_model import CompoundCreate, CompoundOut, CompoundUpdate
from src.services.compound_service import (
    create_compound,
    list_compounds,
    get_compound_by_id,
    update_compound,
    delete_compound,
    search_compounds,
    get_low_stock_compounds,
    get_expiring_compounds
)

router = APIRouter(prefix="/compounds", tags=["Compounds"])

@router.post("/", response_model=CompoundOut)
def add_compound_route(compound: CompoundCreate):
    try:
        return create_compound(compound)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CompoundOut])
def get_all_compounds_route():
    return list_compounds()

@router.get("/{id}", response_model=CompoundOut)
def get_compound_route(id: str):
    try:
        return get_compound_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Compound not found")

@router.put("/{id}", response_model=CompoundOut)
def update_compound_route(id: str, compound: CompoundUpdate):
    try:
        return update_compound(id, compound)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=400, detail=f"Error updating compound: {str(e)}")




@router.delete("/{id}")
def delete_existing_compound_route(id: str):
    try:
        delete_compound(id)
        return {"message": f"Compound {id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/search", response_model=list[CompoundOut])
def search_compounds_endpoint(query: str):
    try:
        return search_compounds(query)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error searching compounds")

@router.get("/low-stock", response_model=list[CompoundOut])
def get_low_stock_compounds_endpoint():
    try:
        return get_low_stock_compounds()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error fetching low stock compounds")

@router.get("/expiring", response_model=list[CompoundOut])
def get_expiring_compounds_endpoint(days: int = 30):
    try:
        return get_expiring_compounds(days)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error fetching expiring compounds")
