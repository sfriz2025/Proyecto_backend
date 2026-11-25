from datetime import datetime, timedelta, timezone

import jwt

from .config import ACCESS_TOKEN_MINUTOS, JWT_SECRET

ALGORITMO = "HS256"


def crear_access_token(usuario_id: int) -> str:
    vencimiento = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_MINUTOS
    )
    datos = {
        "sub": str(usuario_id),
        "exp": vencimiento,
        "type": "access",
    }
    return jwt.encode(datos, JWT_SECRET, algorithm=ALGORITMO)


def leer_access_token(token: str) -> str:
    datos = jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[ALGORITMO],
        options={"require": ["sub", "exp", "type"]},
    )
    if datos["type"] != "access":
        raise jwt.InvalidTokenError("El token debe ser de acceso.")
    return datos["sub"]