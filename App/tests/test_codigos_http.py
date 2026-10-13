import pytest
from fastapi.testclient import TestClient
from App.main import app

client = TestClient(app)

# ==========================================
# 🟢 PRUEBAS DE ÉXITO (2xx)
# ==========================================

def test_201_crear_platillo():
    """Verifica respuesta 201 Created al crear un platillo"""
    payload = {
        "nombre": "Platillo QA Test",
        "categoria": "comida_rapida",
        "precio_restaurante": 5000,
        "tiempo_restaurante_min": 10,
        "costo_estimado_casa": 8000,
        "tiempo_casa_min": 30
    }
    response = client.post("/api/v1/platillos/", json=payload)
    assert response.status_code == 201

def test_200_obtener_platillo():
    """Verifica respuesta 200 OK al obtener un platillo"""
    # Primero creamos uno para asegurar que exista un ID válido
    payload = {
        "nombre": "Platillo Consulta",
        "categoria": "comida_rapida",
        "precio_restaurante": 4000,
        "tiempo_restaurante_min": 10,
        "costo_estimado_casa": 6000,
        "tiempo_casa_min": 20
    }
    res_crear = client.post("/api/v1/platillos/", json=payload)
    platillo_id = res_crear.json()["id"]

    # Consultamos el platillo creado
    response = client.get(f"/api/v1/platillos/{platillo_id}")
    assert response.status_code == 200

def test_204_eliminar_platillo():
    """Verifica respuesta 204 No Content al eliminar un platillo"""
    payload = {
        "nombre": "Platillo a Borrar",
        "categoria": "comida_rapida",
        "precio_restaurante": 3000,
        "tiempo_restaurante_min": 10,
        "costo_estimado_casa": 5000,
        "tiempo_casa_min": 15
    }
    res_crear = client.post("/api/v1/platillos/", json=payload)
    platillo_id = res_crear.json()["id"]

    response = client.delete(f"/api/v1/platillos/{platillo_id}")
    assert response.status_code in [200, 204]


# ==========================================
# 🔴 PRUEBAS DE ERROR (4xx)
# ==========================================

def test_404_platillo_inexistente():
    """Verifica respuesta 404 al buscar o eliminar un ID que no existe"""
    response = client.get("/api/v1/platillos/999999")
    assert response.status_code == 404

def test_422_error_esquema_datos_invalidos():
    """Verifica respuesta 422 si los datos enviados son de tipo incorrecto"""
    payload = {
        "nombre": "Platillo Invalido",
        "precio_restaurante": "texto_en_vez_de_numero"  # Genera error 422
    }
    response = client.post("/api/v1/platillos/", json=payload)
    assert response.status_code == 422