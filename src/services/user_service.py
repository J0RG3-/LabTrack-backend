from supabase import create_client
from src.security import create_access_token, hash_password, verify_password
from src.models.user_model import UserCreate, UserOut
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_user(user: UserCreate) -> UserOut:
    hashed_pwd = hash_password(user.password)

    try:
        response = supabase.table("users").insert({
            "username": user.username,
            "password": hashed_pwd,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }).execute()
    except Exception as e:
        raise Exception(f"Error creando usuario: {e}")

    if not response.data or len(response.data) == 0:
        raise Exception("No se creó el usuario correctamente.")

    user_data = response.data[0]
    return UserOut(**user_data)


def authenticate_user(username: str, password: str):
    try:
        res = supabase.table("users").select("*").eq("username", username).single().execute()
    except Exception:
        return None

    if not res.data:
        return None

    user = res.data
    if not verify_password(password, user["password"]):
        return None

    token = create_access_token({"sub": str(user["id"]), "role": user["role"]})
    return token, user


def get_user_by_id(user_id: str) -> UserOut:
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    if hasattr(response, "error") and response.error:
        raise Exception(f"Error en la consulta: {response.error}")

    if response.data is None:
        raise Exception("Usuario no encontrado")

    return UserOut(**response.data)

