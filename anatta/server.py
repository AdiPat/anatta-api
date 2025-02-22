import sys
from .core.printer import Printer as printer
from .framework import get_server, init_server
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

app = get_server()

start_status = init_server(app)

if start_status:
    printer.print_green_message("Anatta API: Server successfully started.")
else:
    printer.print_red_message("Anatta API: Server failed to start.")
    sys.exit(1)
