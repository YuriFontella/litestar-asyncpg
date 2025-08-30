from __future__ import annotations

from dependency_injector import containers, providers

from src.infrastructure.repositories.asyncpg_user_repository import AsyncpgUserRepository
from src.infrastructure.repositories.asyncpg_session_repository import AsyncpgSessionRepository
from src.infrastructure.repositories.asyncpg_team_repository import AsyncpgTeamRepository
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.application.use_cases.create_team import CreateTeamUseCase
from src.application.use_cases.list_teams import ListTeamsUseCase


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    # Repositories
    user_repository = providers.Factory(AsyncpgUserRepository)
    session_repository = providers.Factory(AsyncpgSessionRepository)
    team_repository = providers.Factory(AsyncpgTeamRepository)

    # Use Cases
    register_user_uc = providers.Factory(
        RegisterUserUseCase, user_repo=user_repository
    )
    authenticate_user_uc = providers.Factory(
        AuthenticateUserUseCase, user_repo=user_repository, session_repo=session_repository
    )
    create_team_uc = providers.Factory(
        CreateTeamUseCase, team_repo=team_repository
    )
    list_teams_uc = providers.Factory(
        ListTeamsUseCase, team_repo=team_repository
    )

