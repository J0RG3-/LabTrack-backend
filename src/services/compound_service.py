import datetime
from supabase import create_client
from src.models.compound_model import CompoundCreate, CompoundOut, CompoundUpdate
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_compound(compound: CompoundCreate) -> CompoundOut:
    response = supabase.table("compounds").insert(compound.dict()).execute()

    if response.status_code != 201:
        raise Exception("No se pudo crear el compuesto.")

    return CompoundOut(**response.data[0])

def list_compounds() -> list[CompoundOut]:
    response = supabase.table("compounds").select("*").execute()

    return [CompoundOut(**item) for item in response.data]

def get_compound_by_id(id: str) -> CompoundOut:
    response = supabase.table("compounds").select("*").eq("id", id).single().execute()

    if response.status_code != 200 or not response.data:
        raise Exception("Compuesto no encontrado.")

    return CompoundOut(**response.data)

def update_compound(id: str, compound: CompoundUpdate) -> CompoundOut:
    data = compound.model_dump()
    if "id" in data:
        del data["id"]
    print("chat  data=", data)
    
    response = supabase.table("compounds").update(data).eq("id", id).execute()
    print("Update response:", response)

    if not response.data or len(response.data) == 0:
        raise Exception("No se pudo actualizar el compuesto: Sin datos")

    return CompoundOut(**response.data[0])




def delete_compound(id: str):
    response = supabase.table("compounds").delete().eq("id", id).execute()
    
    if not response or not getattr(response, "data", None):
        raise Exception("No se pudo eliminar el compuesto o no existe.")
    print(response)
    print(response.__dict__)
    return response.data[0]


def search_compounds(query: str) -> list[CompoundOut]:
    response = supabase.table("compounds").select("*").ilike("name", f"%{query}%").execute()

    return [CompoundOut(**item) for item in response.data]

def get_low_stock_compounds() -> list[CompoundOut]:
    response = supabase.table("compounds").select("*").lte("quantity", "threshold").execute()

    return [CompoundOut(**item) for item in response.data]

def get_expiring_compounds(days: int = 30) -> list[CompoundOut]:
    future_date = (datetime.datetime.now() + datetime.timedelta(days=days)).date()

    response = supabase.table("compounds").select("*").lte("expiry_date", future_date).execute()

    return [CompoundOut(**item) for item in response.data]
