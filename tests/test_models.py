import pytest
from datetime import datetime
from pydantic import ValidationError
from models.voice_payload import VoicePayload
from models.infrastructure import InfrastructureAsset

def test_voice_payload_valid_creation():
    """Verify that VoicePayload accepts valid structural data successfully."""
    payload_data = {
        "asset_type": "Bridge",
        "latitude": -18.1416,
        "longitude": 178.4419,
        "severity": 3,
        "description": "Minor structural wear observed on southern pylons.",
        "timestamp": datetime.utcnow(),
        "confidence_score": 0.95
    }
    payload = VoicePayload(**payload_data)
    assert payload.asset_type == "Bridge"
    assert payload.severity == 3
    assert payload.confidence_score == 0.95

def test_voice_payload_invalid_severity():
    """Verify that VoicePayload raises ValidationError for out-of-range severity levels."""
    payload_data = {
        "asset_type": "Bridge",
        "latitude": -18.1416,
        "longitude": 178.4419,
        "severity": 6,  # Invalid: max is 5
        "description": "Invalid severity check.",
        "timestamp": datetime.utcnow(),
        "confidence_score": 0.90
    }
    with pytest.raises(ValidationError):
        VoicePayload(**payload_data)

    payload_data["severity"] = 0  # Invalid: min is 1
    with pytest.raises(ValidationError):
        VoicePayload(**payload_data)

def test_infrastructure_asset_valid_creation():
    """Verify that InfrastructureAsset maps correctly to Supabase schema expectations."""
    asset = InfrastructureAsset(
        id="test-uuid-1234",
        asset_type="Power Substation",
        geom={"type": "Point", "coordinates": [178.4, -18.1]},
        status="Operational"
    )
    assert asset.id == "test-uuid-1234"
    assert asset.status == "Operational"
    assert asset.geom["type"] == "Point"