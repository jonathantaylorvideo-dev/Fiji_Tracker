import pytest
from services.cache_manager import CacheManager

def test_cache_manager_retrieval():
    """Verify CacheManager returns expected metadata structure and utilizes caching mechanics."""
    # Clear cache prior to test
    CacheManager.clear_caches()
    
    key = "fiji_central_hub"
    result1 = CacheManager.get_cached_metadata(key)
    
    assert result1["key"] == key
    assert result1["region"] == "Fiji"
    assert result1["coordinate_system"] == "EPSG:4326"
    assert result1["status"] == "cached_active"

    # Verify cache hit returns identical dictionary structure
    result2 = CacheManager.get_cached_metadata(key)
    assert result1 == result2