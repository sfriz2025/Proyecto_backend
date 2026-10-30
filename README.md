# FoodCart API

API para registrar cuentas, comparar el costo de restaurante y casa, gestionar productos de platillos y seguir pedidos. La persistencia usa SQLAlchemy y SQLite por defecto; se puede cambiar a PostgreSQL mediante `DATABASE_URL`.

## Equipo y distribución de trabajo

| Integrante | Área | Responsabilidad |
|---|---|---|
| Scarleth Friz (Líder) | Coordinación y seguimiento, dominio y datos | Servidor y Base de Datos con Docker, requirements, .env .example, toda la carpeta infrastructure/ (modelos ORM, mappers, repositoriosSQL), Alembic y seeders. También gestiona ramas y Pull Requests, junto con revisar la lista de verificación antes de entregar. |
| Catalina Ojeda | API y lógica de negocio, calidad y pruebas, documentación e integración. | Reorganizar las carpetas por capas, adaptar servicios y routers a la sesión de Base de Datos, documentar los 6 casos de prueba, README, diagramas y diapositivas. |

## Requisitos e instalación

- Python 3.10 o superior
- `pip`
- Docker 29.9.2
- posgrest:16-alpine

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

La configuración inicial usa `sqlite:///./foodcart.db`. Para PostgreSQL, edita `.env` con una URL como `postgresql+psycopg://usuario:clave@localhost:5432/foodcart` y asegúrate de que la base exista.

## Base de datos, migraciones y datos de ejemplo

```powershell
alembic upgrade head
python -m seeders.seed
uvicorn App.main:app --reload
```

El seeder inserta dos registros de cada entidad y no vuelve a insertar si ya hay cuentas. Para revisar el esquema: `alembic current`; para retroceder: `alembic downgrade base`. La base SQLite se guarda en `foodcart.db` y está excluida de Git.

## Capas

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| Presentación | `App/routers`, `App/schemas` | HTTP, validación de entrada y contratos OpenAPI |
| Aplicación | `App/services`, `App/services/dtos` | Casos de uso, reglas y coordinación |
| Dominio | `App/domain` | Entidades, enums y reglas centrales |
| Infraestructura | `App/infrastructure`, `App/repositories` | Sesiones SQLAlchemy, ORM, mapeo y acceso a datos |

## Recorrido de una solicitud

```mermaid
sequenceDiagram
    participant C as Cliente
    participant R as Router
    participant S as Servicio
    participant D as Depends: sesión
    participant Repo as Repositorio SQL
    participant DB as SQLite/PostgreSQL
    C->>R: Solicitud HTTP
    R->>D: Solicita servicio
    D->>DB: Abre sesión por solicitud
    D->>S: Construye servicio y repositorios
    S->>Repo: Ejecuta caso de uso
    Repo->>DB: Consulta o transacción SQL
    DB-->>Repo: Filas / resultado
    Repo-->>S: Entidad de dominio
    S-->>R: DTO de respuesta
    R-->>C: JSON y código HTTP
```

## Modelo de datos

```mermaid
erDiagram
    CUENTAS ||--o{ PEDIDOS : realiza
    PLATILLOS ||--o{ PEDIDOS : solicitado
    PLATILLOS ||--o{ PRODUCTOS : contiene
    CUENTAS { int id PK string correo UK }
    PLATILLOS { int id PK string nombre UK }
    PRODUCTOS { int id PK int platillo_id FK }
    PEDIDOS { int id PK int cuenta_id FK int platillo_id FK }
```

## Clases principales

```mermaid
classDiagram
    class Cuenta
    class Platillo
    class Producto
    class Pedido
    Cuenta "1" --> "0..*" Pedido
    Platillo "1" --> "0..*" Producto
    Platillo "1" --> "0..*" Pedido
    class CuentaRepository
    class PlatilloRepository
    class ProductoRepository
    class PedidoRepository
    class CuentaService
    class PlatilloService
    class ProductoService
    class PedidoService
    CuentaService --> CuentaRepository
    PlatilloService --> PlatilloRepository
    ProductoService --> ProductoRepository
    PedidoService --> PedidoRepository
```

## API y documentación

Con la aplicación activa, Swagger UI está en `/docs`, ReDoc en `/redoc` y el esquema OpenAPI en `/openapi.json`. Los routers documentan parámetros, modelos, códigos de error y ejemplos de datos en los schemas.

## Pruebas manuales

Abre `tests_manual/foodcart.http` en REST Client de VS Code y ejecuta las solicitudes en orden; la colección Postman está en `tests_manual/collection.json`. Registra el resultado real tras ejecutar cada caso; la columna “Obtenido” queda pendiente de ejecución y no se completa con resultados supuestos.

| Caso | Solicitud | Esperado | Obtenido |
|---|---|---|---|
| Crear platillo | `POST /platillos` con datos válidos | 201 y platillo con ID | Pendiente de ejecutar |
| Listar filtrando | `GET /platillos?categoria=pastas&pagina=1&limite=1` | 200, resultado filtrado y total correcto | Pendiente de ejecutar |
| Correo duplicado | Crear cuenta con correo ya registrado | 409 con formato uniforme de error | Pendiente de ejecutar |
| Regla de negocio | Crear pedido que excede el presupuesto | 400 con detalle de la regla | Pendiente de ejecutar |
| Recurso inexistente | `GET /cuentas/999999` | 404 con formato uniforme de error | Pendiente de ejecutar |
| Validación de entrada | Crear platillo con precio cero | 422 con formato uniforme de error | Pendiente de ejecutar |
| Persistencia tras reinicio | Crear cuenta, detener y levantar Uvicorn, volver a consultar su ID | 200 y mismos datos después del reinicio | Pendiente de ejecutar |

## Errores HTTP

Las respuestas de error mantienen `{ "error": { "code", "message", "details" } }`.

| Código | Uso |
|---|---|
| 200 | Consulta o actualización correcta |
| 201 | Recurso creado |
| 204 | Eliminación sin contenido |
| 400 | Regla de negocio incumplida |
| 404 | Recurso inexistente |
| 409 | Conflicto con el estado o dato duplicado |
| 422 | Validación del esquema |

## Entregables de equipo pendientes

PENDIENTE
