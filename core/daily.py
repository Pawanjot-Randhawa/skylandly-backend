import random
from datetime import datetime, timezone
from typing import Optional
from services.skylanders_data import SkylandersDataService

class Daily:
    @classmethod
    def get_daily_guess(cls, date_str: Optional[str] = None) -> str:
        """Daily Skylander using date-based seeding"""
        # Use provided date for local-day gameplay, otherwise fall back to UTC
        today = date_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        skylanders = SkylandersDataService().get_skylander_names()
        
        if not skylanders:
            raise ValueError("No Skylanders loaded")
        
        # Seed with date ensures same result all day
        random.seed(today)
        return random.choice(skylanders)
    
    @classmethod
    def get_daily_guess_object(cls, date_str: Optional[str] = None):
        """Get full daily Skylander object"""
        name = cls.get_daily_guess(date_str)
        return SkylandersDataService().get_skylander(name)