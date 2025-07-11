import logging
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.models.transaction_model import TransactionCreate, TransactionOut
from src.services.transaction_service import (
    register_transaction,       
    list_transactions,
    get_transactions_by_compound,
    get_transactions_by_instance,
    update_transaction,
    delete_transaction,
    get_transaction_statistics,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=list[TransactionOut])
def get_all_transactions(
    compoundId: Optional[str] = None,
    instanceId: Optional[str] = None,
    type: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    _limit: Optional[int] = Query(None, alias="_limit"),
    _page: Optional[int] = Query(None, alias="_page"),
    _sort: Optional[str] = Query(None, alias="_sort"),
    _order: Optional[str] = Query(None, alias="_order"),
):
    params = {
        "compoundId": compoundId,
        "instanceId": instanceId,
        "type": type,
        "startDate": startDate,
        "endDate": endDate,
        "_limit": _limit,
        "_page": _page,
        "_sort": _sort,
        "_order": _order,
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        return list_transactions(params)
    except Exception as e:
        logging.error(f"list_transactions error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compound/{compound_id}", response_model=list[TransactionOut])
def get_by_compound(compound_id: str):
    try:
        return get_transactions_by_compound(compound_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/instance/{instance_id}", response_model=list[TransactionOut])
def get_by_instance(instance_id: str):
    try:
        return get_transactions_by_instance(instance_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=TransactionOut)
def add_transaction(transaction: TransactionCreate):
    try:
        return register_transaction(transaction)      # ← usa la función correcta
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=TransactionOut)
def update_transaction_endpoint(id: str, updates: TransactionCreate):
    try:
        return update_transaction(id, updates)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}")
def delete_transaction_endpoint(id: str):
    try:
        return delete_transaction(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/statistics")
def get_statistics(
    compoundId: Optional[str] = None,
    instanceId: Optional[str] = None,
    type: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
):
    filters = {
        "compoundId": compoundId,
        "instanceId": instanceId,
        "type": type,
        "startDate": startDate,
        "endDate": endDate,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    try:
        return get_transaction_statistics(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
