from pydantic import TypeAdapter


def dataclass_to_json[T](obj: object) -> bytes:
    adapter = TypeAdapter(type(obj))  # type: ignore[reportUnknownVariableType]
    return adapter.dump_json(obj)  # type: ignore[reportUnknownMemberType]


def dataclass_from_json[T](cls: type[T], json_str: str | bytes) -> T:
    adapter = TypeAdapter(cls)
    return adapter.validate_json(json_str)
