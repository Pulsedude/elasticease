from onstart import OnStart  
from rich.console import Console
from src.user_command import user_command_handler

console = Console()
on_startup = OnStart()

def main():
    # display intro
    on_startup.intro()
    
    # display available options
    on_startup.display_commands()
    
    # display connection status
    on_startup.display_connection_status()
    # call user command handler to allow user to perform various operations
    user_command_handler()
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(e, style="bold red")
        print() 
        