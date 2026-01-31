from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.database import Base


class Player(Base):
	__tablename__ = "players"

	id = Column(Integer, primary_key=True, index=True)
	browser_id = Column(String, unique=True, index=True, nullable=False)
	created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
	last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
	current_streak = Column(Integer, default=0)
	highest_streak = Column(Integer, default=0)
	total_games_played = Column(Integer, default=0)
	total_wins = Column(Integer, default=0)
	last_played_date = Column(Date, nullable=True)

	results = relationship(
		"DailyResult",
		back_populates="player",
		cascade="all, delete-orphan",
	)


class DailyResult(Base):
	__tablename__ = "daily_results"
	__table_args__ = (
		UniqueConstraint("player_id", "date", name="uq_player_date"),
	)

	id = Column(Integer, primary_key=True, index=True)
	player_id = Column(Integer, ForeignKey("players.id"), index=True, nullable=False)
	date = Column(Date, index=True, nullable=False)
	won = Column(Boolean, default=False)
	guess_count = Column(Integer, nullable=False, default=0)
	skylander_name = Column(String, nullable=True)
	finished_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

	player = relationship("Player", back_populates="results")
	guesses = relationship(
		"Guess",
		back_populates="daily_result",
		cascade="all, delete-orphan",
		order_by="Guess.guess_index",
	)


class Guess(Base):
	__tablename__ = "guesses"

	id = Column(Integer, primary_key=True, index=True)
	daily_result_id = Column(Integer, ForeignKey("daily_results.id"), index=True, nullable=False)
	guess_index = Column(Integer, nullable=False)
	guess_name = Column(String, nullable=False)
	created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

	daily_result = relationship("DailyResult", back_populates="guesses")
