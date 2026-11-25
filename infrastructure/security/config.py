import os

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "").strip()
ACCESS_TOKEN_MINUTOS = int(os.getenv("ACCESS_TOKEN_MINUTOS", "15"))

if not JWT_SECRET:
    raise RuntimeError("Falta configurar JWT_SECRET en el entorno.")

if ACCESS_TOKEN_MINUTOS <= 0:
    raise ValueError("ACCESS_TOKEN_MINUTOS debe ser mayor que cero.")