import pytest
from unittest.mock import MagicMock, patch
from services.gemini_client import GeminiVoiceParser
from services.supabase_client import SupabaseService
from models.database import QueryResponse

@patch("services.gemini_client.genai.GenerativeModel")
@patch("services.gemini_client.settings")
def test_gemini_voice_parser_success(mock_settings, mock_generative_model):
    """Test successful transcript parsing with mocked Gemini API response."""
    mock_settings.GEMINI_API_KEY = "fake-api-key"
    
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"asset_type": "Roadway", "latitude": -17.7, "longitude": 178.0, "severity": 2, "description": "Minor washout", "timestamp": "2026-07-26T12:00:00", "confidence_score": 0.98}'
    mock_model_instance.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model_instance

    parser = GeminiVoiceParser()
    payload = parser.parse_transcript("Test transcript text")

    assert payload is not None
    assert payload.asset_type == "Roadway"
    assert payload.severity == 2
    assert payload.confidence_score == 0.98

@patch("services.supabase_client.create_client")
@patch("services.supabase_client.settings")
def test_supabase_service_fetch_failure_handling(mock_settings, mock_create_client):
    """Test graceful error handling when Supabase database fetch drops or raises an exception."""
    mock_settings.SUPABASE_URL = "https://fake.supabase.co"
    mock_settings.SUPABASE_KEY = "fake-key"

    mock_client = MagicMock()
    mock_client.table.side_effect = Exception("Database connection dropped")
    mock_create_client.return_value = mock_client

    service = SupabaseService()
    response = service.fetch_all_assets()

    assert response.success is False
    assert "Database connection dropped" in response.error