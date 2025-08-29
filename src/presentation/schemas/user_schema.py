from typing import Optional
from msgspec import Struct

# Importando as entidades comuns
from src.domain.entities.common import User, Session, Token
from src.domain.entities.base import BaseEntity


class UserCreateSchema(BaseEntity, kw_only=True):
    """Schema para criação de usuário."""
    name: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = True
    email: str
    password: str
    
    def to_entity(self) -> User:
        """Converte o schema para entidade User."""
        return User(**self.to_dict())


class UserResponseSchema(BaseEntity, kw_only=True):
    """Schema para resposta de usuário."""
    role: Optional[str] = None
    id: int
    name: str
    email: str
    status: bool
    
    @classmethod
    def from_entity(cls, entity: User) -> 'UserResponseSchema':
        """Cria um schema a partir de uma entidade User."""
        return cls(**entity.to_dict())


class UserLoginSchema(BaseEntity, kw_only=True):
    """Schema para login de usuário."""
    email: str
    password: str
    
    def to_entity(self) -> User:
        """Converte o schema para entidade User."""
        return User(**self.to_dict())


class TokenSchema(BaseEntity, kw_only=True):
    """Schema para token."""
    token: str
    
    @classmethod
    def from_entity(cls, entity: Token) -> 'TokenSchema':
        """Cria um schema a partir de uma entidade Token."""
        return cls(**entity.to_dict())