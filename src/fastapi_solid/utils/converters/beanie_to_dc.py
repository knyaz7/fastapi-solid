from dataclasses import fields, is_dataclass

from beanie import Document


def to_dataclass[T](obj: Document, cls: type[T]) -> T:
    """Build a dataclass instance from an ODM document"""
    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")

    data = {}
    for f in fields(cls):
        data[f.name] = getattr(obj, f.name)
    return cls(**data)
