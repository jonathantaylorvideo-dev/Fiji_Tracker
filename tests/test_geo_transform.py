import pytest
from utils.geo_transform import transform_coordinates, validate_fiji_bounds

def test_transform_coordinates_valid():
    """Verify that coordinate transforms correctly format latitude and longitude pairs."""
    lat, lon = -18.1416, 178.4419  # Suva, Fiji coordinates
    transformed = transform_coordinates(lat, lon)
    assert transformed is not None
    assert isinstance(transformed, tuple)
    assert transformed[0] == lat
    assert transformed[1] == lon

def test_validate_fiji_bounds_inside():
    """Verify that coordinates within Fiji's regional box pass validation."""
    # Fiji roughly spans latitudes -15 to -22 and longitudes 177 to -178 (177 to 180 / -180 to -178 across the 180th meridian)
    lat, lon = -18.1416, 178.4419
    assert validate_fiji_bounds(lat, lon) is True

def test_validate_fiji_bounds_outside():
    """Verify that coordinates outside Fiji trigger bounds warnings or validation failure."""
    lat, lon = 38.8951, -77.0364  # Washington, D.C.
    assert validate_fiji_bounds(lat, lon) is False