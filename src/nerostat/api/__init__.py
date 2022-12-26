from fastapi import APIRouter
from .player import router as get_player_by_stat_router

router = APIRouter()
router.include_router(get_player_by_stat_router)
