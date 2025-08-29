from dependency_injector import containers, providers

from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.repositories.user_repository import UserRepository, SessionRepository
from src.infrastructure.repositories.team_repository import TeamRepository, PlayerRepository
from src.application.use_cases.user_use_case import UserUseCase
from src.application.use_cases.team_use_case import TeamUseCase


class Container(containers.DeclarativeContainer):
    # Configuração
    config = providers.Configuration()
    
    # Infraestrutura
    db_connection = providers.Singleton(DatabaseConnection)
    
    # Repositórios
    user_repository = providers.Factory(
        UserRepository,
        db_connection=db_connection
    )
    
    session_repository = providers.Factory(
        SessionRepository,
        db_connection=db_connection
    )
    
    team_repository = providers.Factory(
        TeamRepository,
        db_connection=db_connection
    )
    
    player_repository = providers.Factory(
        PlayerRepository,
        db_connection=db_connection
    )
    
    # Casos de uso
    user_use_case = providers.Factory(
        UserUseCase,
        user_repository=user_repository,
        session_repository=session_repository
    )
    
    team_use_case = providers.Factory(
        TeamUseCase,
        team_repository=team_repository,
        player_repository=player_repository
    )