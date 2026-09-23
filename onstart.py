from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from src.config import read
from rich import box
from src.commands import (
    core_commands,
    crud_commands
)
import requests
import urllib3
import sys

# disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

class OnStart:
    def __init__(self):
        # read ascii.txt to display ASCII text on the top
        self.ascii_text = "\n\n"
        with open("./ascii.txt", "r", encoding="utf-8") as file:
            self.ascii_text += file.read()
        
        
    def intro(self):
        # display ascii text first
        console.print(self.ascii_text, style="cyan")
        print() # for gap
        console.print(
            Panel.fit(
                Text.from_markup(
                    "[bold cyan]elasticease[/bold cyan] is an interactive CLI for working with "
                    "Elasticsearch from your terminal.\n\n"
                    "It is built to make common cluster tasks easier: check cluster health, "
                    "ping your configured Elasticsearch node, inspect shards, indices, nodes, "
                    "master node details, and storage capacity. It also provides a simple "
                    "command style for index and document operations such as creating or "
                    "deleting indices, adding documents, viewing documents, and updating "
                    "existing records.\n\n"
                    "Connection settings are read from [bold]config.yaml[/bold]. "
                    "Type [bold]exit[/bold], [bold]quit[/bold], or [bold]q[/bold] to close the tool."
                ),
                border_style="cyan",
            )
        )
        print() # for gap

    def display_commands(self):
        core_commands_table = Table(
            show_header=True,
            header_style="bold bright_cyan",
            expand=True,
            box=box.SIMPLE_HEAVY,
            pad_edge=False
        )
        
        core_commands_table.add_column("command")
        core_commands_table.add_column("purpose")
        core_commands_table.add_column("example")
        
        for command in core_commands:
            argument = command.get("arguments").get("required")
            
            core_commands_table.add_row(
                f"[bold]{command.get("name") if argument is None else command.get("name") + " " + argument}[/bold]",
                command.get("purpose"),
                command.get("example") if command.get("example") else "-"
            )
        
        # CRUD operations commands
        crud_commands_table = Table(
            show_header=True,
            header_style="bold bright_cyan",
            expand=True,
            box=box.SIMPLE_HEAVY,
            pad_edge=False
        )
        
        crud_commands_table.add_column("command")
        crud_commands_table.add_column("purpose")
        crud_commands_table.add_column("example")
        
        for command in crud_commands:
            argument = command.get("arguments").get("required")
            
            crud_commands_table.add_row(
                f"[bold]{command.get("name") if argument is None else command.get("name") + " " + argument}[/bold]",
                command.get("purpose"),
                command.get("example") if command.get("example") else "-",
                
            )
        
        # core commands panel
        core_commands_panel = Panel(
            core_commands_table,
            title="Core commands",
            box=box.ROUNDED,
            border_style="yellow"
        )
        
        # crud commands panel
        crud_commands_panel = Panel(
            crud_commands_table,
            title="CRUD commands",
            box=box.ROUNDED,
            border_style="yellow"
        )
        
        # group of core and crud commands panel
        commands_group = Group(
            core_commands_panel,
            crud_commands_panel,
        )
        console.print(Panel(commands_group, title="Available options", border_style="bright_yellow", box=box.ROUNDED))
    
    def verify_connection(self, base_url: str, auth: tuple):
        try:
            try:
                response = requests.get(
                    url=base_url,
                    timeout=10,
                    auth=auth,
                    verify=False
                )
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
            if response.status_code != 200:
                return False
            return True
        except Exception as e:
            return (False, e)
        
    def display_connection_status(self):
        configuration = read().get("elasticease")
        base_url = None if isinstance(configuration, tuple) else configuration.get("elasticsearch").get("base_url")
        username = None if isinstance(configuration, tuple) else configuration.get("elasticsearch").get("username")
        password = None if isinstance(configuration, tuple) else configuration.get("elasticsearch").get("password")
        
        if base_url is None:
            console.print(f"elasticsearch base_url is {base_url}\nPlease check the elasticsearch base_url in the configuration and then try again!", style="red")
            sys.exit(1)
            
        status = f"[bold]Base URL:[/bold] [bright_blue]{base_url}[/bright_blue]\n[bold]Connection:[/bold] "
        
        # check connection
        auth = (username, password)
        connection = self.verify_connection(base_url, auth)
        
        if isinstance(connection, tuple):
            console.print(connection[1], style="bold red")
            return  
        
        status += "🔴" if not connection else "🟢"
        
        console.print(status)
        
        
        
        