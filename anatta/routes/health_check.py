from fastapi import APIRouter
from anatta.models import HealthCheckResponse

health_check_router = APIRouter()


@health_check_router.get("/health_check")
async def health_check():
    """
    Standard health check endpoint for the Anatta API.

    Args:
        None

    Returns:
        dict: A dictionary containing the status of the API.
    """
    return HealthCheckResponse(status="ok", message="Anatta API is running.")
