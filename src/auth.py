from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt            # pip install python-jose
from datetime import datetime, timezone
from config import settings as cf         # tu settings/ENV con SECRET_KEY, ALGORITHM
from src.services.user_service import get_user_by_id  # utilízalo si quieres devolver el usuario
from src.models.user_model import UserOut               # o el modelo que uses

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserOut:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            cf.SECRET_KEY,
            algorithms=["HS256"],   # p.e. "HS256"
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token sin ID de usuario",
            )
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    # 🔸 Si solo necesitas el ID puedes devolverlo directamente
    # return int(user_id)

    # 🔸 Si quieres el objeto usuario completo (recomendado):
    user = get_user_by_id(user_id)        # implementa o reutiliza tu función
    return user
