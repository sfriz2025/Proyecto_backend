import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from infrastructure.database import Base, get_db

# Base de datos SQLite en memoria: aislada y rápida
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 

@pytest.fixture()
def db_session():
    """Crea las tablas antes de cada test y las destruye al terminar."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """Cliente HTTP de FastAPI conectado a la base de datos de prueba."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

#¿Por qué se hace? Para tener una base de datos limpia y aislada en cada prueba, sin tocar jamás los datos reales de PostgreSQL.
#¿Por qué así? Porque si un test deja basura en la base de datos (por ejemplo, un correo ya registrado), haría fallar al siguiente test. Con yield y drop_all, cada test parte desde cero y es 100% reproducible. (Nota: cuando integren el pipeline de CI/CD, asegúrense de que las pruebas de integración también validen contra una BD preparada con migraciones de Alembic, tal como pide la rúbrica).
