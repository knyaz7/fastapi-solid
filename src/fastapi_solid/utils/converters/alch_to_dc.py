from dataclasses import fields, is_dataclass

from fastapi_solid.infrastructure.sqlalchemy.setup.base_model import Base


def to_dataclass[T](obj: Base, cls: type[T]) -> T:
    """Builds dataclass from ORM-model"""
    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")

    data = {}
    for f in fields(cls):
        data[f.name] = getattr(obj, f.name)
    return cls(**data)
