from fastapi import APIRouter

from .v1.players import players_router
from .v1.users import users_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(users_router)
api_v1_router.include_router(players_router)
