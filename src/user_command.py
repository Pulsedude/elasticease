from rich.console import Console
from rich.prompt import Prompt
import sys

console = Console()

def user_command_handler():
    """User command handler to allow user to perform various operations through available commands
    """
    try:
        while True:
            try:
                user_input = Prompt.ask("[yellow]>[/yellow][cyan]>[/cyan][blue]>[/blue] ")
                
                if not user_input:
                    continue
                
                elif user_input.lower() in ("exit", "quit", "q", "ex"):
                    console.print("See ya!", style="bold")
                    sys.exit(0)
                    
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
    except Exception as e:
        console.print(e, style="bold red")