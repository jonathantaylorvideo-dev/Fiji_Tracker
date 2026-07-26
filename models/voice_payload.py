from datetime import datetime
from pydantic import BaseModel, Field

class VoicePayload(BaseModel):
    """Pydantic model validating structured JSON parsed from audio transcripts by Gemini."""
    asset_type: str = Field(..., description="Type of infrastructure asset (e.g., bridge, road, power line)")
    latitude: float = Field(..., description="Latitude coordinate of the asset")
    longitude: float = Field(..., description="Longitude coordinate of the asset")
    severity: int = Field(..., ge=1, le=5, description="Severity rating from 1 (minor) to 5 (critical)")
    description: str = Field(..., description="Detailed description of the infrastructure issue or asset status")
    timestamp: datetime = Field(..., description="Timestamp when the event or inspection occurred")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the transcription and extraction")