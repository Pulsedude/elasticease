from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from src.commands import (
    core_commands,
    crud_command
)

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
                    "[bold cyan]ElasticEase[/bold cyan] is an interactive CLI for working with "
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
            title="Core Commands",
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
            core_commands_table.add_row(
                command.get("name"),
                command.get("purpose"),
                command.get("example") if command.get("example") else "-"
            )
        