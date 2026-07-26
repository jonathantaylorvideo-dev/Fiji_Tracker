from core.logger import get_logger

logger = get_logger()

def sanitize_payload(payload: str) -> str:
    """Sanitize string inputs to defend against injection or malformed strings."""
    try:
        if not isinstance(payload, str):
            return str(payload)
        return payload.strip().replace("\x00", "")
    except Exception as e:
        logger.error(f"Error sanitizing payload: {e}")
        return ""