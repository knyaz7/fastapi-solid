from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 10
    offset: int = 0
