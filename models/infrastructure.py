from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any

class InfrastructureAsset(BaseModel):
    """Pydantic data contract representing a tracked infrastructure asset in Fiji with adaptive schema mapping."""
    id: Optional[str] = Field(None, description="Unique identifier for the asset")
    asset_id: Optional[str] = Field(None, description="Alias for id")
    name: Optional[str] = Field("Unnamed Asset", description="Name or designation of the infrastructure element")
    asset_type: str = Field(..., description="Category of the asset (e.g., Bridge, Power Line, Road)")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Geographic latitude")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Geographic longitude")
    severity: Optional[int] = Field(3, ge=1, le=5, description="Urgency/severity rating from 1 to 5")
    geom: Optional[Dict[str, Any]] = Field(None, description="GeoJSON geometry object")
    description: Optional[str] = Field(None, description="Detailed field notes or remarks")
    status: str = Field("Active", description="Operational status of the asset")

    @model_validator(mode='before')
    @classmethod
    def reconcile_fields(cls, data: Any) -> Any:
        """Automatically bridges id/asset_id and extracts lat/lon from GeoJSON geom objects if provided."""
        if isinstance(data, dict):
            if 'id' in data and not data.get('asset_id'):
                data['asset_id'] = data['id']
            elif 'asset_id' in data and not data.get('id'):
                data['id'] = data['asset_id']

            geom = data.get('geom')
            if isinstance(geom, dict) and 'coordinates' in geom:
                coords = geom['coordinates']
                if isinstance(coords, list) and len(coords) >= 2:
                    if data.get('longitude') is None:
                        data['longitude'] = coords[0]
                    if data.get('latitude') is None:
                        data['latitude'] = coords[1]
        return data