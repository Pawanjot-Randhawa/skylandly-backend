from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class HistoryResultUpsertRequest(BaseModel):
    browser_id: str = Field(..., min_length=1)
    date: Optional[str] = None
    won: bool
    guess_count: int = Field(..., ge=0)
    skylander_name: Optional[str] = None
    guesses: Optional[List[str]] = None
    current_streak: Optional[int] = Field(default=None, ge=0)
    highest_streak: Optional[int] = Field(default=None, ge=0)
    total_games_played: Optional[int] = Field(default=None, ge=0)
    total_wins: Optional[int] = Field(default=None, ge=0)
    last_played_date: Optional[str] = None


class HistoryResultResponse(BaseModel):
    date: date
    won: bool
    guess_count: int
    skylander_name: Optional[str] = None
    guesses: List[str] = Field(default_factory=list)


class HistorySummaryResponse(BaseModel):
    current_streak: int
    highest_streak: int
    total_games_played: int
    total_wins: int


class AverageGuessesResponse(BaseModel):
    average_guesses: float
    total_games: int


class HistoryGameResponse(BaseModel):
    date: date
    won: bool
    guess_count: int
    skylander_name: Optional[str] = None
    guesses: List[str] = Field(default_factory=list)


class HistoryGamesResponse(BaseModel):
    games: List[HistoryGameResponse]
