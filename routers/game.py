from fastapi import APIRouter, Depends, HTTPException

from core.daily import Daily
from schemas.skylanders import GuessResponse
from services.game import Game

router = APIRouter(
    prefix="/game",
    tags=["game"],
)

@router.post("/guess", response_model=GuessResponse)
def make_guess(skylander_name: str):
    """
    Endpoint to make a guess about a Skylander.
    """
    if not Game.is_valid_skylander(skylander_name):
        raise HTTPException(status_code=400, detail="Invalid Skylander name")
    
    comparison = Game.compare_skylanders(skylander_name)
    is_correct = skylander_name.lower() == Daily.get_daily_guess().lower()
    return GuessResponse(
        correct=is_correct,
        comparison=comparison
    )

@router.get("/daily")
def get_daily():
    """Get today's daily Skylander (without spoilers for frontend)"""
    return {"skylander_name": Daily.get_daily_guess()}