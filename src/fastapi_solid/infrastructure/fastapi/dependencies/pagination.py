from fastapi import Query

from fastapi_solid.application.interfaces.common.pagination import Pagination


def get_pagination(
    limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)
) -> Pagination:
    return Pagination(limit=limit, offset=offset)
