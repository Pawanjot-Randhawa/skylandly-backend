import random
from datetime import datetime
from services.skylanders_data import SkylandersDataService

class Daily:
    @classmethod
    def get_daily_guess(cls) -> str:
        """Daily Skylander using date-based seeding"""
        # Use today's date as seed for reproducibility
        today = datetime.now().strftime("%Y-%m-%d")
        
        skylanders = SkylandersDataService().get_skylander_names()
        
        if not skylanders:
            raise ValueError("No Skylanders loaded")
        
        # Seed with date ensures same result all day
        random.seed(today)
        return random.choice(skylanders)
    
    @classmethod
    def get_daily_guess_object(cls):
        """Get full daily Skylander object"""
        name = cls.get_daily_guess()
        return SkylandersDataService().get_skylander(name)