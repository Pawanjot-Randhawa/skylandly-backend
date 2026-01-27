# services/skylanders_data.py
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from schemas.skylanders import SkylanderInfo

logger = logging.getLogger(__name__)

class SkylandersDataService:
    """Service for loading and managing Skylanders data"""
    
    _data: Dict[str, SkylanderInfo] = {}
    _loaded = False
    
    @classmethod
    def load_data(cls) -> None:
        """Load Skylanders data from JSON file into memory"""
        if cls._loaded:
            logger.info("Skylanders data already loaded.")
            return
        
        data_path = Path(__file__).parent.parent / "data" / "skylandersdb.json"
        logger.info(f"Loading Skylanders from: {data_path}")
        
        try:
            with open(data_path, 'r') as f:
                raw_data = json.load(f)
            
            logger.info(f"Raw JSON contains: {len(raw_data)} entries")
            cls._data.clear()
            
            # Convert raw JSON to SkylanderInfo objects
            for name, attributes in raw_data.items():
                cls._data[name.lower()] = SkylanderInfo(
                    name=name,
                    element=attributes.get("element", ""),
                    gender=attributes.get("gender", ""),
                    game=attributes.get("game", ""),
                    species=attributes.get("species", "")
                )
            
            cls._loaded = True
            logger.info(f"✓ Loaded {len(cls._data)} Skylanders into memory")
        
        except FileNotFoundError:
            logger.error(f"✗ Error: skylandersdb.json not found at {data_path}")
            raise
        except Exception as e:
            logger.error(f"✗ Error loading Skylanders data: {e}", exc_info=True)
            raise
    
    @classmethod
    def get_skylander(cls, name: str) -> Optional[SkylanderInfo]:
        """Get a Skylander by name (case-insensitive)"""
        if not cls._loaded:
            cls.load_data()
        return cls._data.get(name.lower())
    
    @classmethod
    def get_all_skylanders(cls) -> List[SkylanderInfo]:
        """Get all Skylanders"""
        if not cls._loaded:
            cls.load_data()
        return list(cls._data.values())
    
    @classmethod
    def get_skylander_names(cls) -> List[str]:
        """Get list of all Skylander names"""
        if not cls._loaded:
            cls.load_data()
        return list(cls._data.keys())
    
    @classmethod
    def is_valid_skylander(cls, name: str) -> bool:
        """Check if a Skylander name exists"""
        if not cls._loaded:
            cls.load_data()
        is_valid = name.lower() in cls._data
        logger.debug(f"Validating '{name}': {is_valid} (total skylanders: {len(cls._data)})")
        return is_valid
    
    @classmethod
    def get_skylanders_by_element(cls, element: str) -> List[SkylanderInfo]:
        """Get all Skylanders of a specific element"""
        if not cls._loaded:
            cls.load_data()
        return [s for s in cls._data.values() if s.element.lower() == element.lower()]
    
    @classmethod
    def get_skylanders_by_gender(cls, gender: str) -> List[SkylanderInfo]:
        """Get all Skylanders of a specific gender"""
        if not cls._loaded:
            cls.load_data()
        return [s for s in cls._data.values() if s.gender.lower() == gender.lower()]