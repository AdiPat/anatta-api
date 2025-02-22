import traceback
from fastapi import FastAPI
from .core.printer import Printer as printer
from .routes.health_check import health_check_router
from .routes.daily_teaching import daily_teaching_router


def get_server() -> FastAPI:
    """
    Generate a FastAPI server instance and return it.

    Args:
        None

    Returns:
        FastAPI: A FastAPI server instance.
    """
    try:
        app = FastAPI()
        return app
    except Exception as e:
        printer.print_red_message(f"Error in get_server: {e}")
        traceback.print_exc()
        return None


def init_server(app: FastAPI) -> bool:
    """
    Initialize the FastAPI server instance and return it.

    Args:
        None

    Returns:
        bool: True if the server is successfully initialized, False otherwise.
    """
    try:
        app.include_router(health_check_router)
        app.include_router(daily_teaching_router)
        return True
    except Exception as e:
        printer.print_red_message(f"Error in init_server: {e}")
        traceback.print_exc()
        return False
