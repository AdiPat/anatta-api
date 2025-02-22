from langchain_community.utilities import GoogleSerperAPIWrapper
import traceback
import os
from anatta.core.printer import Printer as printer
from uuid import uuid4
from typing import Dict
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

serper = GoogleSerperAPIWrapper(serper_api_key=os.environ.get("SERPER_API_KEY"))


def search_internet(query: str) -> Dict:
    """
    Searches the internet using Google Serper API.

    Args:
        query: The search query.

    Returns:
        str: The search results in JSON format.
    """
    global serper
    request_id = uuid4()
    try:
        search = serper
        search_results = search.results(query)
        return {
            "request_id": request_id,
            "search_results": search_results,
            "error": None,
        }
    except Exception as e:
        printer.print_red_message(f"Error searching the internet: {e}")
        traceback.print_exc()
        return {
            "request_id": request_id,
            "search_results": None,
            "error": f"Failed to search the internet due to unexpected error: {e}",
        }
