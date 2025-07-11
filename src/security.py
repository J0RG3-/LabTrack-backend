# src/core/security.py
import os
from datetime import datetime, timedelta
import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()  # lee las variables de .env

# ───────────────────────────
# CONSTANTES DE CONFIGURACIÓN
# ───────────────────────────
SECRET_KEY = os.getenv("JWT_SECRET", "change_me")       # cambia en producción
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)        # duración por defecto: 60 min
)

# ───────────────────────────
# FUNCIONES DE CONTRASEÑA
# ───────────────────────────
def hash_password(plain_password: str) -> str:
    """Devuelve un hash bcrypt del password en texto plano."""
    return bcrypt.hashpw(plain_password.encode("utf-8"),
                         bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comprueba si el password plano coincide con el hash almacenado."""
    return bcrypt.checkpw(plain_password.encode("utf-8"),
                          hashed_password.encode("utf-8"))

# ───────────────────────────
# FUNCIONES JWT
# ───────────────────────────
def create_access_token(data: dict,
                        expires_delta: int | None = None) -> str:
    """
    Genera un JWT con los datos proporcionados.
    - `data`: payload (p.ej. {"sub": user_id, "role": "admin"})
    - `expires_delta`: minutos de validez; si None usa configuración por defecto.
    """
    to_encode = data.copy()
    exp_minutes = expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=exp_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodifica un JWT y devuelve el payload.
    Lanza jwt.ExpiredSignatureError o jwt.InvalidTokenError si no es válido.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


