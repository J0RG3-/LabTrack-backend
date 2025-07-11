from datetime import date, datetime
from supabase import create_client
from src.models.count_session_model import CountSessionCreate, CountSessionOut
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_count_session(session: CountSessionCreate, user_id: int) -> CountSessionOut:
    data = session.model_dump(exclude_unset=True)
    data.setdefault("created_by", user_id)
    data.setdefault("start_date", date.today().isoformat())

    response = supabase.table("count_sessions").insert(data).execute()
    if not response.data or len(response.data) == 0:
        raise Exception("No se pudo crear la sesión (sin datos devueltos).")
    return CountSessionOut(**response.data[0])


def list_count_sessions() -> list[CountSessionOut]:
    response = (
        supabase.table("count_sessions")
        .select("*")
        .order("start_date", desc=True)
        .execute()
    )

    if response.error:
        raise Exception(f"Error al listar sesiones: {response.error.message}")

    return [CountSessionOut(**item) for item in response.data]


def get_count_session_by_id(session_id: str) -> CountSessionOut:
    response = (
        supabase.table("count_sessions")
        .select("*")
        .eq("id", session_id)
        .single()
        .execute()
    )

    if response.error or response.data is None:
        raise Exception(f"Sesión con ID {session_id} no encontrada.")

    return CountSessionOut(**response.data)


def update_count_session(session_id: str, session: CountSessionCreate) -> CountSessionOut:
    data = session.model_dump(exclude_unset=True)
    data["updated_at"] = datetime.utcnow().isoformat()

    response = (
        supabase.table("count_sessions")
        .update(data)
        .eq("id", session_id)
        .execute()
    )

    if response.error or not response.data:
        raise Exception(f"No se pudo actualizar la sesión {session_id}: {response.error}")

    return CountSessionOut(**response.data[0])


def delete_count_session(session_id: str) -> CountSessionOut:
    session = get_count_session_by_id(session_id)

    response = (
        supabase.table("count_sessions")
        .delete()
        .eq("id", session_id)
        .execute()
    )

    if response.error:
        raise Exception(f"No se pudo eliminar la sesión {session_id}: {response.error}")

    return session
