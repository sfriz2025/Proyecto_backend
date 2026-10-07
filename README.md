### Proyecto grupal: diseño e implementación de una API backend (15%)


### Anatomia del Proyecto

app/
   main.py # crea y configura la aplicación
   routers/ # recibe solicitudes HTTP
   schemas/ # DTO y validaciones
   domain/ # entidades y reglas del dominio
   services/ # casos de uso y reglas de negocio
   repositories/ # almacenamiento en memoria
tests_manual/ # colección Postman, Thunder Client o archivo .http
README.md
requirements.txt o pyproject.tom

### Organización de Grupo

| Área de responsabilidad | Responsabilidad principal |
| :--- | :--- |
| **Coordinación y seguimiento** | Organización del backlog, seguimiento de tareas, reuniones, control de avances e integración de entregables. |
| **Dominio y datos** | Modelado de entidades, relaciones, DTO, validaciones y coherencia del modelo del dominio. |
| **API y lógica de negocio** | Implementación de endpoints, servicios, reglas de negocio y manejo de errores. |
| **Calidad y pruebas** | Verificación funcional de endpoints, casos exitosos y de error, colección de pruebas y revisión del funcionamiento general. |
| **Documentación e integración** | Swagger/OpenAPI, README, documentación técnica y revisión de la integración de los distintos componentes del proyecto. |

| Estudiante | Responsabilidad principal |
| :--- | :--- |
| **Catalina Ojeda** | Coordinación + documentación e integración |
| **Sebastián Ulloa** | Dominio y datos |
| **Scarleth Friz** | API y lógica de negocio |
| **Genesis Flores** | Calidad y pruebas |

### Respuesta a Errores 

| Código | Definición obligatoria |
| :--- | :--- |
| **200 OK** | Consulta, actualización o eliminación correcta cuando se devuelve contenido. |
| **201 Created** | Recurso creado correctamente. |
| **204 No Content** | Eliminación correcta cuando no se devuelve contenido. |
| **400 Bad Request** | La solicitud es comprensible, pero viola una regla de negocio. |
| **404 Not Found** | El recurso solicitado no existe. |
| **409 Conflict** | La operación entra en conflicto con el estado actual, por ejemplo un registro duplicado. |
| **422 Unprocessable Entity** | Los datos no cumplen el esquema o las validaciones declaradas. |