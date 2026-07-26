from typing import Tuple

def transform_coordinates(lat: float, lon: float) -> Tuple[float, float]:
    """Formats or transforms latitude and longitude coordinate pairs."""
    return (float(lat), float(lon))

def validate_fiji_bounds(lat: float, lon: float) -> bool:
    """Validates whether given coordinates fall within Fiji's regional bounding box."""
    if not (-22.0 <= lat <= -15.0):
        return False
    
    is_east_hemisphere = (176.0 <= lon <= 180.0)
    is_west_hemisphere = (-180.0 <= lon <= -176.0)
    
    return is_east_hemisphere or is_west_hemisphere