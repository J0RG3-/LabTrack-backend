import datetime
from supabase import create_client
from src.models.compound_instance_model import CompoundInstanceCreate, CompoundInstanceOut
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_instance(instance: CompoundInstanceCreate) -> CompoundInstanceOut:
    data = instance.dict(exclude_unset=True)
    response = supabase.table("compound_instances").insert(data).execute()

    if response.status_code != 201:
        raise Exception("No se pudo crear la instancia del compuesto.")

    return CompoundInstanceOut(**response.data[0])

def list_instances(params: dict = {}) -> list[CompoundInstanceOut]:
    response = supabase.table("compound_instances").select("*").execute()

    # Filtrado adicional según los parámetros recibidos, si es necesario
    if params:
        # Este es un ejemplo de filtrado. Si necesitas más parámetros, ajusta el código.
        response.data = [item for item in response.data if all(item[key] == value for key, value in params.items())]

    return [CompoundInstanceOut(**item) for item in response.data]

def get_instance_by_id(instance_id: str) -> CompoundInstanceOut:
    response = supabase.table("compound_instances").select("*").eq("id", instance_id).single().execute()
    if not response.data:
        raise Exception(f"Instance with ID {instance_id} not found.")
    return CompoundInstanceOut(**response.data)

def get_instances_by_compound_id(compound_id: str) -> list[CompoundInstanceOut]:
    response = supabase.table("compound_instances").select("*").eq("compound_id", compound_id).execute()
    return [CompoundInstanceOut(**item) for item in response.data]

def update_instance(instance_id: str, updates: CompoundInstanceCreate) -> CompoundInstanceOut:
    data = updates.dict(exclude_unset=True)
    response = supabase.table("compound_instances").update(data).eq("id", instance_id).execute()

    if response.status_code != 200:
        raise Exception(f"Error updating instance with ID {instance_id}.")
    
    return CompoundInstanceOut(**response.data[0])

def delete_instance(instance_id: str) -> CompoundInstanceOut:
    response = supabase.table("compound_instances").delete().eq("id", instance_id).execute()

    if response.status_code != 200:
        raise Exception(f"Error deleting instance with ID {instance_id}.")
    
    return CompoundInstanceOut(**response.data[0])

def get_low_stock_instances() -> list[CompoundInstanceOut]:
    # Este método filtra las instancias con bajo stock basándose en el campo `quantity`.
    response = supabase.table("compound_instances").select("*").execute()
    low_stock_instances = [item for item in response.data if item.get("quantity", 0) <= item.get("threshold", 0)]
    return [CompoundInstanceOut(**item) for item in low_stock_instances]

def get_expiring_instances(days: int = 30) -> list[CompoundInstanceOut]:
    future_date = (datetime.datetime.now() + datetime.timedelta(days=days)).isoformat()
    response = supabase.table("compound_instances").select("*").lte("expiry_date", future_date).execute()
    return [CompoundInstanceOut(**item) for item in response.data]

def get_instances_by_location(location: str) -> list[CompoundInstanceOut]:
    response = supabase.table("compound_instances").select("*").eq("location", location).execute()
    return [CompoundInstanceOut(**item) for item in response.data]

def update_instance_quantity(instance_id: str, quantity: int) -> CompoundInstanceOut:
    response = supabase.table("compound_instances").update({"quantity": quantity}).eq("id", instance_id).execute()

    if response.status_code != 200:
        raise Exception(f"Error updating quantity for instance with ID {instance_id}.")
    
    return CompoundInstanceOut(**response.data[0])

def mark_instance_as_used_up(instance_id: str) -> CompoundInstanceOut:
    response = supabase.table("compound_instances").update({"status": "used_up", "quantity": 0}).eq("id", instance_id).execute()

    if response.status_code != 200:
        raise Exception(f"Error marking instance with ID {instance_id} as used-up.")
    
    return CompoundInstanceOut(**response.data[0])

def search_instances(query: str) -> list[CompoundInstanceOut]:
    response = supabase.table("compound_instances").select("*").ilike("batch_number", f"%{query}%").execute()
    return [CompoundInstanceOut(**item) for item in response.data]
