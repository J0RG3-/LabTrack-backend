from fastapi import APIRouter, HTTPException
from src.models.compound_instance_model import CompoundInstanceCreate, CompoundInstanceOut
from src.services.compound_instance_service import (
    create_instance,
    list_instances,
    get_instance_by_id,
    get_instances_by_compound_id,
    update_instance,
    delete_instance,
    get_low_stock_instances,
    get_expiring_instances,
    get_instances_by_location,
    update_instance_quantity,
    mark_instance_as_used_up,
    search_instances,
)

router = APIRouter(prefix="/compoundInstances", tags=["Compound Instances"])

@router.post("/", response_model=CompoundInstanceOut)
def add_instance(instance: CompoundInstanceCreate):
    try:
        return create_instance(instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CompoundInstanceOut])
def get_all_instances(params: dict = {}):
    return list_instances(params)

@router.get("/{id}", response_model=CompoundInstanceOut)
def get_instance(id: str):
    try:
        return get_instance_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Instance {id} not found: {str(e)}")

@router.get("/compound/{compound_id}", response_model=list[CompoundInstanceOut])
def get_instances_by_compound(compound_id: str):
    try:
        return get_instances_by_compound_id(compound_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No instances found for compound {compound_id}: {str(e)}")

@router.put("/{id}", response_model=CompoundInstanceOut)
def update_instance(id: str, updates: CompoundInstanceCreate):
    try:
        return update_instance(id, updates)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", response_model=CompoundInstanceOut)
def delete_instance(id: str):
    try:
        return delete_instance(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Instance {id} not found: {str(e)}")

@router.get("/low-stock", response_model=list[CompoundInstanceOut])
def get_low_stock():
    try:
        return get_low_stock_instances()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching low stock instances: {str(e)}")

@router.get("/expiring", response_model=list[CompoundInstanceOut])
def get_expiring(days: int = 30):
    try:
        return get_expiring_instances(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching expiring instances: {str(e)}")

@router.get("/location/{location}", response_model=list[CompoundInstanceOut])
def get_instances_by_location(location: str):
    try:
        return get_instances_by_location(location)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No instances found at location {location}: {str(e)}")

@router.put("/{id}/quantity", response_model=CompoundInstanceOut)
def update_instance_quantity(id: str, quantity: int):
    try:
        return update_instance_quantity(id, quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating quantity for instance {id}: {str(e)}")

@router.put("/{id}/mark-as-used-up", response_model=CompoundInstanceOut)
def mark_instance_as_used_up(id: str):
    try:
        return mark_instance_as_used_up(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error marking instance {id} as used-up: {str(e)}")

@router.get("/search", response_model=list[CompoundInstanceOut])
def search_instances(query: str):
    try:
        return search_instances(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching instances: {str(e)}")
