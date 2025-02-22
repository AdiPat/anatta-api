from uuid import uuid4
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from anatta.models import DailyTeaching
from anatta.core.web_search import search_internet
from datetime import datetime
from anatta.core.printer import Printer as printer
from anatta.core.ai import ai
import json
from typing import Dict, Any

daily_teaching_router = APIRouter()


def get_search_results(query: str) -> Dict[str, Any]:
    """Fetch search results from the internet.

    Args:
        query (str): The search query.

    Returns:
        Dict[str, Any]: The search results.
    """
    try:
        return search_internet(query)
    except Exception as e:
        printer.print_red_message(f"Error searching the internet: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=json.dumps({"error": "Failure when searching the internet."}),
        )


def generate_teaching(prompt: str) -> str:
    """Generate teaching text using AI.

    Args:
        prompt (str): The prompt for AI text generation.

    Returns:
        str: The generated teaching text.
    """
    try:
        return ai.generate_text(prompt=prompt).text
    except Exception as e:
        printer.print_red_message(f"Error generating teaching: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=json.dumps({"error": "Error generating teaching."}),
        )


def generate_teaching_description(prompt: str) -> str:
    """Generate teaching description using AI.

    Args:
        prompt (str): The prompt for AI text generation.

    Returns:
        str: The generated teaching description.
    """
    try:
        return ai.generate_text(prompt=prompt).text
    except Exception as e:
        printer.print_red_message(f"Error generating teaching description: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=json.dumps({"error": "Error generating teaching description."}),
        )


@daily_teaching_router.get("/daily_teaching", response_model=DailyTeaching)
async def daily_teaching() -> DailyTeaching:
    """Standard daily teaching endpoint for the Anatta API.

    Args:
        None

    Returns:
        DailyTeaching: A Pydantic model containing the daily teaching.
    """
    request_id = str(uuid4())
    current_date_formatted = datetime.now().strftime("%Y-%m-%d")
    query = f"Find the top global events today as of {current_date_formatted}."

    search_results = get_search_results(query)
    results = search_results.get("search_results")
    error = search_results.get("error")

    if not results or error:
        printer.print_red_message(f"Error searching the internet: {error}")
        raise HTTPException(
            status_code=500,
            detail=json.dumps(
                {"request_id": request_id, "error": "Unexpected system failure."}
            ),
        )

    teaching_prompt = f"""
        Given the current world events, generate a simple, relevant Buddhist teaching for today.
        Today's date is {current_date_formatted} in YYYY-MM-DD format.
        Reference the search results in your teaching wherever appropriate.
        
        Search Results for query "Find the top global events as of {current_date_formatted} in YYYY-MM-DD format":
        '''
        {json.dumps(results, indent=4)}
        '''
    """
    teaching = generate_teaching(teaching_prompt)

    description_prompt = f"""
        Given the teaching of the day, provide a brief description of the teaching.
        Today's date is {current_date_formatted} in YYYY-MM-DD format.
        Teaching of the Day:
        '''
        {teaching}
        '''
    """
    teaching_description = generate_teaching_description(description_prompt)

    return DailyTeaching(
        request_id=request_id,
        date=current_date_formatted,
        title=f"Daily Teaching for {current_date_formatted}",
        teaching=teaching,
        teaching_description=teaching_description,
    )
