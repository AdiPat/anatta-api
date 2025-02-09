from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    A Pydantic model for the health check response.

    Args:
        BaseModel: The base Pydantic model class.
    """

    status: str
    message: str
