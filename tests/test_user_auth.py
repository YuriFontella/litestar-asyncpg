import pytest
from unittest.mock import AsyncMock, patch
from litestar.testing import TestClient

from app import app
from src.domain.entities.common import User, Session
from src.presentation.schemas.user_schema import UserCreateSchema, UserLoginSchema


@pytest.fixture
def client():
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def mock_user():
    return User(
        id=1,
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        role="user",
        status="active"
    )


@pytest.fixture
def mock_session():
    return Session(
        id=1,
        user_id=1,
        access_token="test_token",
        user_agent="test_agent",
        client_ip="127.0.0.1",
        revoked=False,
        created_at="2023-01-01T00:00:00"
    )


@patch('src.application.use_cases.user_use_case.UserUseCase.register')
async def test_user_registration(mock_register, client, mock_user):
    """Test user registration"""
    # Configure mock
    mock_register.return_value = mock_user
    
    # Test registration
    response = client.post(
        "/api/v1/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@example.com"


@patch('src.application.use_cases.user_use_case.UserUseCase.authenticate')
async def test_user_login(mock_authenticate, client, mock_user, mock_session):
    """Test user login"""
    # Configure mock
    mock_authenticate.return_value = (mock_user, mock_session, "jwt_token")
    
    # Test login
    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token" in response.json()