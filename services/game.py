from schemas.skylanders import SkylanderInfo, CompareResult, AttributeComparison
from core.daily import Daily
from services.skylanders_data import SkylandersDataService

class Game:
    data_service = SkylandersDataService()

    @classmethod
    def is_valid_skylander(cls, name: str) -> bool:
        """Check if a Skylander name is valid """
        return cls.data_service.is_valid_skylander(name)

    @classmethod
    def compare_skylanders(cls, guess: str) -> dict:
        """Compare user's guess with daily Skylander"""

        daily_skylander = Daily.get_daily_guess_object()
        user_skylander = cls.data_service.get_skylander(guess)

        if not daily_skylander:
            raise ValueError(f"Daily Skylander '{daily_skylander}' not found")

        return CompareResult(
            name=AttributeComparison(
                value=user_skylander.name,
                is_correct=user_skylander.name.lower() == daily_skylander.name.lower()
            ),
            element=AttributeComparison(
                value=user_skylander.element,
                is_correct=user_skylander.element.lower() == daily_skylander.element.lower()
            ),
            gender=AttributeComparison(
                value=user_skylander.gender,
                is_correct=user_skylander.gender.lower() == daily_skylander.gender.lower()
            ),
            game=AttributeComparison(
                value=user_skylander.game,
                is_correct=user_skylander.game.lower() == daily_skylander.game.lower()
            ),
            species=AttributeComparison(
                value=user_skylander.species,
                is_correct=user_skylander.species.lower() == daily_skylander.species.lower()
            )
        )