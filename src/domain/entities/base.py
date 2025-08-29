from typing import Optional, List, Any, Type, TypeVar, cast
from datetime import datetime
from decimal import Decimal
from msgspec import Struct
from dataclasses import dataclass, field

# Tipo genérico para as entidades
T = TypeVar('T')

# Classe base para entidades usando msgspec
class BaseEntity(Struct, kw_only=True, omit_defaults=True):
    """Classe base para todas as entidades usando msgspec."""
    
    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """Converte um dicionário para uma instância da entidade."""
        return cast(T, cls(**data))
    
    def to_dict(self) -> dict:
        """Converte a entidade para um dicionário."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

# Adaptadores para converter entre diferentes representações
def entity_to_schema(entity: Any, schema_class: Type[T]) -> T:
    """Converte uma entidade para um schema."""
    return schema_class(**entity.to_dict())

def schema_to_entity(schema: Any, entity_class: Type[T]) -> T:
    """Converte um schema para uma entidade."""
    return entity_class(**{k: v for k, v in schema.__dict__.items() if not k.startswith('_')})