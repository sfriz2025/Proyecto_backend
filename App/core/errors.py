"""Errores controlados de la API y formato JSON uniforme (sección 5.4 de la pauta)."""
from typing import Any, List, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException


# ---- Modelos solo para documentar los errores en Swagger ----
class ErrorCuerpo(BaseModel):
    code: str
    message: str
    details: List[Any] = Field(default_factory=list)

    
class ErrorResponse(BaseModel):
    error: ErrorCuerpo


# ---- Excepciones que lanzan los servicios ----
class AppError(Exception):
    status_code = 400
    code = "BUSINESS_RULE_VIOLATION"

    def __init__(self, message: str, details: Optional[List[Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details if details is not None else []



class NotFoundError(AppError):
    status_code = 404
    code = "RESOURCE_NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"


class BusinessRuleError(AppError):
    status_code = 400
    code = "BUSINESS_RULE_VIOLATION"


# ---- Manejadores: todos devuelven {"error": {code, message, details}} ----
def _respuesta(status_code: int, code: str, message: str, details: Optional[List[Any]] = None):
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details if details is not None else []}},
    )


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _manejar_app_error(request: Request, exc: AppError):
        return _respuesta(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(RequestValidationError)
    async def _manejar_validacion(request: Request, exc: RequestValidationError):
        detalles = []
        for e in exc.errors():
            ruta = [str(p) for p in e.get("loc", []) if p not in ("body", "query", "path")]
            detalles.append({"campo": ".".join(ruta) or None, "mensaje": str(e.get("msg", ""))})
        return _respuesta(
            422, "VALIDATION_ERROR", "Los datos enviados no cumplen las validaciones", detalles
        )

    @app.exception_handler(StarletteHTTPException)
    async def _manejar_http(request: Request, exc: StarletteHTTPException):
        codigos = {404: "RESOURCE_NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}
        return _respuesta(exc.status_code, codigos.get(exc.status_code, "HTTP_ERROR"), str(exc.detail))
