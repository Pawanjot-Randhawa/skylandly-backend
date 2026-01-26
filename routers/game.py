from fastapi import APIRouter, Depends, HTTPException

from schemas.skylanders import GuessResponse


router = APIRouter(
    prefix="/game",
    tags=["game"],
)

@router.post("/guess", response_model=GuessResponse)
def make_guess(skylander_name: str):
    """
    Endpoint to make a guess about a Skylander.
    """
    # Placeholder implementation
    if skylander_name.lower() == "spyro":
        comparison = {
            "element": "Fire",
            "gender": "Male",
            "game": "Skylanders: Spyro's Adventure"
        }
        return GuessResponse(correct=True, comparison=comparison)
    else:
        comparison = {
            "element": "Unknown",
            "gender": "Unknown",
            "game": "Unknown"
        }
        return GuessResponse(correct=False, comparison=comparison)