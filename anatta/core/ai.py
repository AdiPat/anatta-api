import traceback
import os
import json
from openai import OpenAI
from anatta.core.printer import Printer as printer
from uuid import uuid4
from anatta.models import GenerateTextResponse


class AI:
    """
    A facade class for the OpenAI API.
    """

    DEFAULT_SYSTEM = "You are a helpful assistant."
    DEFAULT_TEMPERATURE = 0.5
    DEFAULT_MAX_TOKENS = 1024
    DEFAULT_VERBOSE = False

    def __init__(self, verbose=DEFAULT_VERBOSE):
        """
        Initializes the AI class.
        """
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.verbose = verbose
        self.id = str(uuid4())

        if self.verbose:
            printer.print_bright_green_message(f"AI initialized: {self.id}")

    def generate_text(
        self,
        prompt: str,
        system=DEFAULT_SYSTEM,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    ) -> GenerateTextResponse:
        """
        Generates text using the OpenAI API.

        Args:
            system (str): The system to use for generating text.
            prompt (str): The prompt to use for generating text.
            temperature (float): The temperature to use for generating text.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated text.
        """
        request_id = str(uuid4())
        try:
            if self.verbose:
                log_params = {
                    "request_id": request_id,
                    "prompt": prompt,
                    "system": system,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
                log_params_json = json.dumps(log_params, indent=4)
                printer.print_bright_green_message(
                    f"Generating text: {request_id}: {log_params_json}"
                )
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            text = response.choices[0].message.content
            if self.verbose:
                printer.print_bright_green_message(f"Generated text: {text}")
            return GenerateTextResponse(request_id=request_id, text=text, error="")
        except Exception as e:
            printer.print_bright_red_message(f"Error generating text: {e}")
            traceback.print_exc()
            error = f"Response generation failed due to error: {e}"
            return GenerateTextResponse(
                request_id=request_id,
                text="Failed to generate response due to unexpected error.",
                error=error,
            )


ai = AI(verbose=True)
