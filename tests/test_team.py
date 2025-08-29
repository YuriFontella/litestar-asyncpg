import pytest
from unittest.mock import AsyncMock, patch
from litestar.testing import TestClient

from app import app
from src.domain.entities.common import Team, Player
from src.presentation.schemas.team_schema import TeamSchema


@pytest.fixture
def client():
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def mock_players():
    return [
        Player(
            id=1,
            name="Player 1",
            team_id=1,
            language="pt-br",
            uuid="uuid1",
            status="active"
        ),
        Player(
            id=2,
            name="Player 2",
            team_id=1,
            language="en",
            uuid="uuid2",
            status="active"
        )
    ]


@pytest.fixture
def mock_team(mock_players):
    return Team(
        id=1,
        name="Test Team",
        price=100.0,
        owner="test@example.com",
        protocol="TEST123",
        date="2023-01-01T00:00:00",
        players=mock_players
    )


@patch('src.application.use_cases.team_use_case.TeamUseCase.create_team_with_players')
async def test_create_team(mock_create_team, client, mock_team):
    """Test team creation with players"""
    # Configure mock
    mock_create_team.return_value = mock_team
    
    # Test team creation
    response = client.post(
        "/api/v1/teams",
        json={
            "name": "Test Team",
            "price": 100.0,
            "owner": "test@example.com",
            "players": [
                {
                    "name": "Player 1",
                    "language": "pt-br",
                    "uuid": "uuid1",
                    "status": "active"
                },
                {
                    "name": "Player 2",
                    "language": "en",
                    "uuid": "uuid2",
                    "status": "active"
                }
            ]
        }
    )
    
    assert response.status_code == 201
    assert response.json()["name"] == "Test Team"
    assert response.json()["price"] == 100.0
    assert response.json()["owner"] == "test@example.com"
    assert len(response.json()["players"]) == 2


@patch('src.application.use_cases.team_use_case.TeamUseCase.get_all_teams_with_players')
async def test_get_all_teams(mock_get_all_teams, client, mock_team):
    """Test getting all teams with players"""
    # Configure mock
    mock_get_all_teams.return_value = [mock_team]
    
    # Test getting all teams
    response = client.get("/api/v1/teams")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Team"
    assert len(response.json()[0]["players"]) == 2