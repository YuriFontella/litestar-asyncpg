import pytest
from litestar.testing import TestClient

from app import app
from src.core.di import container


@pytest.fixture
def client():
    with TestClient(app=app) as client:
        yield client


def test_app_initialization(client):
    """Test if the application initializes correctly"""
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_dependency_injection():
    """Test if the dependency injection container is correctly configured"""
    # Verifica se os repositórios estão configurados
    assert container.user_repository()
    assert container.session_repository()
    assert container.team_repository()
    assert container.player_repository()
    
    # Verifica se os casos de uso estão configurados
    assert container.user_use_case()
    assert container.team_use_case()