from typing import Dict, Any, Optional
from supabase import create_client, Client
from core.config import settings
from core.logger import get_logger
from models.database import QueryResponse

logger = get_logger()

class SupabaseService:
    """Handles secure database connections and operations with Supabase for infrastructure assets."""

    def __init__(self):
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_KEY
        self.client: Optional[Client] = None

        if not url or not key:
            logger.warning("Supabase credentials (URL or Key) are missing from environment settings.")
            return

        try:
            self.client = create_client(url, key)
            logger.info("Supabase client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self.client = None

    def insert_asset(self, asset_data: Dict[str, Any]) -> QueryResponse:
        """Inserts a new infrastructure asset record into the Supabase database."""
        if not self.client:
            logger.error("Supabase client is uninitialized. Cannot execute insert operation.")
            return QueryResponse(success=False, error="Database client uninitialized")

        try:
            response = self.client.table("infrastructure").insert(asset_data).execute()
            logger.info("Successfully inserted new infrastructure asset record.")
            return QueryResponse(success=True, data=response.data)
        except Exception as e:
            logger.error(f"Database insert error: {e}")
            return QueryResponse(success=False, error=str(e))

    def fetch_all_assets(self) -> QueryResponse:
        """Fetches all infrastructure assets from Supabase with graceful fallback state handling."""
        if not self.client:
            logger.warning("Supabase client unavailable. Returning fallback empty state.")
            return QueryResponse(success=True, data=[])

        try:
            response = self.client.table("infrastructure").select("*").execute()
            logger.info("Successfully retrieved all infrastructure assets.")
            return QueryResponse(success=True, data=response.data)
        except Exception as e:
            logger.error(f"Database fetch error: {e}")
            return QueryResponse(success=False, error=str(e))

    def update_asset_status(self, asset_id: str, new_status: str) -> QueryResponse:
        """Updates the operational status of a specific infrastructure asset record."""
        if not self.client:
            logger.error("Supabase client is uninitialized. Cannot execute update operation.")
            return QueryResponse(success=False, error="Database client uninitialized")

        try:
            response = self.client.table("infrastructure").update({"status": new_status}).eq("id", asset_id).execute()
            logger.info(f"Successfully updated status for asset ID: {asset_id}")
            return QueryResponse(success=True, data=response.data)
        except Exception as e:
            logger.error(f"Database update error: {e}")
            return QueryResponse(success=False, error=str(e))