from functools import lru_cache
from typing import Dict, Any
from core.logger import get_logger

logger = get_logger()

class CacheManager:
    """Lightweight local caching utility to minimize redundant database round-trips for static GIS metadata."""

    @staticmethod
    @lru_cache(maxsize=128)
    def get_cached_metadata(key: str) -> Dict[str, Any]:
        """Retrieves cached metadata based on a static key string."""
        logger.info(f"Cache miss for key: '{key}'. Loading static reference metadata.")
        return {
            "key": key,
            "region": "Fiji",
            "coordinate_system": "EPSG:4326",
            "status": "cached_active"
        }

    @classmethod
    def clear_caches(cls):
        """Clears all in-memory lru_caches managed by the application."""
        try:
            cls.get_cached_metadata.cache_clear()
            logger.info("Successfully cleared static metadata caches.")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")