# 🍔 Food Cart API - Backend para Carrito de Comida

Bienvenido al repositorio de **Food Cart API**, la solución backend desarrollada en FastAPI para la gestión de pedidos, productos y clientes de un carrito de comida rápida.

Este proyecto implementa una API RESTful construida bajo los principios de **Arquitectura en Capas** (Layered Architecture) y almacenamiento en memoria, diseñada para ser escalable, desacoplada y fácil de mantener.

---

## 🛠️ Arquitectura y Estructura del Proyecto

El sistema fue diseñado aplicando la separación de responsabilidades para garantizar un código limpio y modular:

- **Capa de API** (`app/api`): Expone los endpoints HTTP, maneja los códigos de estado (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, etc.) y la documentación interactiva OpenAPI/Swagger.
- **Capa de Servicios** (`app/services`): Contiene la lógica de negocio principal (cálculo de totales, aplicación de reglas de negocio, validación de flujo de estados).
- **Capa de Dominio** (`app/domain`): Define las entidades puras del sistema y las reglas del modelo de datos.
- **Capa de Esquemas / DTOs** (`app/schemas`): Utiliza Pydantic para la entrada y salida de datos, asegurando la validación estricta de tipos y formatos.
- **Capa de Persistencia / Repositorios** (`app/db`): Implementa el patrón Repository para gestionar los datos en memoria (diccionarios/listas) sin acoplarse a una base de datos física.

---

## 🌟 Funcionalidades Principales

### 1. Gestión de Productos (CRUD Completo):
- Crear, listar, consultar por ID, actualizar y eliminar productos del menú.

### 2. Consultas Avanzadas (Filtro, Ordenamiento y Paginación):
- Endpoint de listado optimizado para aplicar filtros por categoría, ordenamiento por precio o nombre, y paginación en un solo Request.

### 3. Gestión de Pedidos y Reglas de Negocio:
- Control de flujo para el cambio de estado de comandas (`pendiente` ➔ `en_preparacion` ➔ `listo` ➔ `entregado`).
- Validaciones automáticas de stock y límites de consumo.

### 4. Manejo Global de Errores:
- Respuestas JSON estandarizadas ante excepciones o datos inválidos (código `422` / `400`).

---

## 🚀 Cómo Ejecutar el Proyecto Localmente

### Prerrequisitos
- Python 3.9 o superior instalado.

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd foodcart_api!
   ```