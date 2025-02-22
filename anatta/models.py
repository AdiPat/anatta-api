from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    A Pydantic model for the health check response.

    Args:
        BaseModel: The base Pydantic model class.
    """

    status: str
    message: str


class GenerateTextResponse(BaseModel):
    """
    A Pydantic model for the generate text response.

    Args:
        BaseModel: The base Pydantic model class.
    """

    request_id: str
    text: str
    error: str


class DailyTeaching(BaseModel):
    """
    A Pydantic model for the daily teaching response.

    Args:
        BaseModel: The base Pydantic model class.
    """

    request_id: str
    date: str
    title: str
    teaching: str
    teaching_description: str
