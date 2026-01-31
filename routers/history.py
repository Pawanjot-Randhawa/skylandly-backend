from datetime import date as date_type, datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from db.database import get_db
from models.history import DailyResult, Guess, Player
from schemas.history import (
    AverageGuessesResponse,
    HistoryGameResponse,
    HistoryGamesResponse,
    HistoryResultResponse,
    HistoryResultUpsertRequest,
    HistorySummaryResponse,
)

router = APIRouter(
    prefix="/history",
    tags=["history"],
)


def _get_or_create_player(db: Session, browser_id: str) -> Player:
    player = db.query(Player).filter(Player.browser_id == browser_id).first()
    now = datetime.now(timezone.utc)
    if player:
        player.last_seen = now
        return player

    player = Player(browser_id=browser_id, created_at=now, last_seen=now)
    db.add(player)
    db.flush()
    return player


def _parse_date(value: str | None) -> date_type | None:
    if not value:
        return None
    try:
        return date_type.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {value}") from exc


@router.post("/result", response_model=HistoryResultResponse)
def upsert_result(payload: HistoryResultUpsertRequest, db: Session = Depends(get_db)):
    if not payload.browser_id:
        raise HTTPException(status_code=400, detail="browser_id is required")

    parsed_date = _parse_date(payload.date)
    game_date = parsed_date or datetime.now(timezone.utc).date()
    player = _get_or_create_player(db, payload.browser_id)

    if payload.current_streak is not None:
        player.current_streak = payload.current_streak
    if payload.highest_streak is not None:
        player.highest_streak = payload.highest_streak
    if payload.total_games_played is not None:
        player.total_games_played = payload.total_games_played
    if payload.total_wins is not None:
        player.total_wins = payload.total_wins
    if payload.last_played_date is not None:
        player.last_played_date = _parse_date(payload.last_played_date)

    result = (
        db.query(DailyResult)
        .filter(DailyResult.player_id == player.id, DailyResult.date == game_date)
        .first()
    )

    if result is None:
        result = DailyResult(
            player_id=player.id,
            date=game_date,
            won=payload.won,
            guess_count=payload.guess_count,
            skylander_name=payload.skylander_name,
            finished_at=datetime.now(timezone.utc),
        )
        db.add(result)
        db.flush()
    else:
        result.won = payload.won
        result.guess_count = payload.guess_count
        result.skylander_name = payload.skylander_name
        result.finished_at = datetime.now(timezone.utc)

    guesses_out: List[str] = []
    if payload.guesses is not None:
        db.query(Guess).filter(Guess.daily_result_id == result.id).delete()
        for idx, name in enumerate(payload.guesses):
            if name:
                db.add(Guess(daily_result_id=result.id, guess_index=idx, guess_name=name))
                guesses_out.append(name)
    else:
        guesses_out = [g.guess_name for g in result.guesses]

    db.commit()
    db.refresh(result)

    return HistoryResultResponse(
        date=result.date,
        won=result.won,
        guess_count=result.guess_count,
        skylander_name=result.skylander_name,
        guesses=guesses_out,
    )




@router.get("/summary", response_model=HistorySummaryResponse)
def get_summary(
    browser_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    player = db.query(Player).filter(Player.browser_id == browser_id).first()
    if not player:
        return HistorySummaryResponse(
            current_streak=0,
            highest_streak=0,
            total_games_played=0,
            total_wins=0,
        )

    return HistorySummaryResponse(
        current_streak=player.current_streak or 0,
        highest_streak=player.highest_streak or 0,
        total_games_played=player.total_games_played or 0,
        total_wins=player.total_wins or 0,
    )


@router.get("/games", response_model=HistoryGamesResponse)
def get_games(
    browser_id: str = Query(..., min_length=1),
    limit: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    player = db.query(Player).filter(Player.browser_id == browser_id).first()
    if not player:
        return HistoryGamesResponse(games=[])

    results = (
        db.query(DailyResult)
        .filter(DailyResult.player_id == player.id)
        .order_by(DailyResult.date.desc())
        .limit(limit)
        .all()
    )

    games = [
        HistoryGameResponse(
            date=r.date,
            won=r.won,
            guess_count=r.guess_count,
            skylander_name=r.skylander_name,
            guesses=[g.guess_name for g in r.guesses],
        )
        for r in results
    ]

    return HistoryGamesResponse(games=games)


@router.get("/average-guesses", response_model=AverageGuessesResponse)
def get_average_guesses(
    browser_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    player = db.query(Player).filter(Player.browser_id == browser_id).first()
    if not player:
        return AverageGuessesResponse(average_guesses=0.0, total_games=0)

    total_games = (
        db.query(func.count(DailyResult.id))
        .filter(DailyResult.player_id == player.id)
        .scalar()
    )

    total_guesses = (
        db.query(func.coalesce(func.sum(DailyResult.guess_count), 0))
        .filter(DailyResult.player_id == player.id)
        .scalar()
    )

    average_guesses = (total_guesses / total_games) if total_games else 0.0

    return AverageGuessesResponse(
        average_guesses=round(float(average_guesses), 2),
        total_games=int(total_games or 0),
    )