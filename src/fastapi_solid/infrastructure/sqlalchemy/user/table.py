from sqlalchemy.orm import Mapped

from fastapi_solid.infrastructure.sqlalchemy.setup.base_model import Base


class UserOrm(Base):
    __tablename__ = "users"

    name: Mapped[str]
