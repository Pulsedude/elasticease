from rich.console import Console
from rich.prompt import Prompt
import sys

# commands logic
# core commands ------
from .core_operations import CoreOps

console = Console()
coreops = CoreOps()

def user_command_handler():
    """User command handler to allow user to perform various operations through available commands
    """
    try:
        print()
        while True:
            try:
                user_input = Prompt.ask("[yellow]>[/yellow][cyan]>[/cyan][bright_blue]>[/bright_blue] ")
                
                if not user_input:
                    continue
                
                # ----------------------------------------------------------------------
                #                       Core Commands handling
                # ----------------------------------------------------------------------
                
                # check elasticsearch cluster health
                elif user_input.lower() == "health":
                    coreops.check_cluster_health()
                    
                # see list of shards
                elif user_input.lower() == "shards":
                    coreops.available_shards()
                    
                # see list of indices
                elif user_input.lower() == "indices":
                    coreops.available_indices()
                    
                # ping to cluster to check health
                elif user_input.lower() == "ping":
                    coreops.ping()
                
                # clear console
                elif user_input.lower() == "clear":
                    print("\033[2J\033[H")
                    
                elif user_input.lower() in ("exit", "quit", "q", "ex"):
                    console.print("See ya!", style="bold")
                    sys.exit(0)
                    
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
    except Exception as e:
        console.print(e, style="bold red")