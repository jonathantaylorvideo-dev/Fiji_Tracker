from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QueryResponse(BaseModel):
    """Generic wrapper for database query execution results."""
    success: bool = Field(..., description="Indicates whether the database operation succeeded")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Returned rows or document records from the query")
    error: Optional[str] = Field(None, description="Detailed error message if the query execution failed")

class PaginationModel(BaseModel):
    """Pagination parameters and metadata for large dataset queries."""
    limit: int = Field(default=50, ge=1, le=1000, description="Number of items per page")
    offset: int = Field(default=0, ge=0, description="Offset for pagination tracking")
    total_count: Optional[int] = Field(None, description="Total matching records available in the database table")