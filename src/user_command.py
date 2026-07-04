from rich.console import Console
from rich.prompt import Prompt
import sys

# utils
from .utils import remove_commas

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
                user_input = Prompt.ask(
                    "[yellow]>[/yellow][cyan]>[/cyan][bright_blue]>[/bright_blue] ")

                if not user_input:
                    continue

                # ----------------------------------------------------------------------
                #                       Core Commands handling
                # ----------------------------------------------------------------------

                # check elasticsearch cluster health
                elif user_input.lower() == "health":
                    coreops.check_cluster_health()

                # see list of shards
                elif user_input.lower().startswith("shards"):
                    command_to_see_all_shards = user_input.split()
                    if len(command_to_see_all_shards) > 1 and command_to_see_all_shards[1].lower() in ("\'json\'", "\"json\"", "json"):
                        coreops.available_shards(json_result=True)
                    else:
                        coreops.available_shards()


                # see list of indices
                elif user_input.lower().startswith("indices"):
                    command_to_see_all_indices = user_input.split()
                    if len(command_to_see_all_indices) > 1 and command_to_see_all_indices[1].lower() in ("\'json\'", "\"json\"", "json"):
                        coreops.available_indices(json_result=True)
                    else:
                        coreops.available_indices()


                # ping to cluster to check health
                elif user_input.lower() == "ping":
                    coreops.ping()


                # see specific index details
                elif user_input.lower().startswith("index"):
                    command_to_see_index_details = user_input.split()
                    if len(command_to_see_index_details) != 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"index <index_name>\" to see the details of any specific index.\n", style="red")
                        continue

                    coreops.index_details(remove_commas(
                        command_to_see_index_details[1]))


                # see list of master nodes
                elif user_input.lower().startswith("master"):
                    command_to_see_master_nodes = user_input.split()
                    if len(command_to_see_master_nodes) > 1 and command_to_see_master_nodes[1].lower() in ("\'json\'", "\"json\"", "json"):
                        coreops.master_nodes(json_result=True)
                    else:
                        coreops.active_nodes()


                # see list of active nodes
                elif user_input.lower().startswith("nodes"):
                    command_to_see_active_nodes = user_input.split()
                    if len(command_to_see_active_nodes) > 1 and command_to_see_active_nodes[1].lower() in ("\'json\'", "\"json\"", "json"):
                        coreops.active_nodes(json_result=True)
                    else:
                        coreops.active_nodes()


                # see storage capacities of active nodes
                elif user_input.lower().startswith("capacity"):
                    command_to_see_nodes_capacity = user_input.split()
                    if len(command_to_see_nodes_capacity) > 1 and command_to_see_nodes_capacity[1].lower() in ("\'json\'", "\"json\"", "json"):
                        coreops.nodes_capacity(json_result=True)
                    else:
                        coreops.nodes_capacity()

                # update or add new elasticsearch base url
                elif user_input.lower().startswith("conn"):
                    command_to_updated_elastic_base_url = user_input.split()
                    if len(command_to_updated_elastic_base_url) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"conn <base_url>\" to add or updated with new Elasticsearch base request URL.\n", style="red")
                        continue
                    
                    coreops.new_password(remove_commas(command_to_updated_elastic_base_url[1]))
                    
                # update or add new elasticsearch password for connection
                elif user_input.lower().startswith("auth"):
                    command_to_update_elastic_password = user_input.split()
                    if len(command_to_update_elastic_password) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"auth <new_password>\" to add or updated elastic password for connection.\n", style="red")
                        continue
                    
                    coreops.new_password(remove_commas(command_to_update_elastic_password[1]))

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
