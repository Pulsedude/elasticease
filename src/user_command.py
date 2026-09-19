from rich.console import Console
from rich.prompt import Prompt
import sys

# utils
from .utils import remove_commas

# core operaitons  ------
from .core_operations import CoreOps

# crud operaitons ------
from .crud_operations import CrudOps

console = Console()
coreops = CoreOps()
crudops = CrudOps()


def user_command_handler():
    """User command handler to allow user to perform various operations through available commands
    """
    def double_argu_command_handler(command: str, action):
        """Special command handler for commands which supports double arguments 
        """
        command_list = command.split()

        if len(command_list) > 2:
            first_argu = remove_commas(
                command_list[1]).lower()
            sec_argu = remove_commas(
                command_list[2]).lower()

            if first_argu == "json":

                if sec_argu == "true":
                    # call that such specific method (function) according to given command
                    action(
                        json_result=True, ai_summarization=True)
                    return

                elif sec_argu == "false":
                    # call that such specific method (function) according to given command
                    action(json_result=True)
                    return 

                else:
                    console.print(
                        "Please use valid argument \"true\" or \"false\" in order to get AI-powered summary\n", style="red")
                    return 

            else:
                console.print(
                    "Please use valid argument \"json\" in order to get JSON format response.\n", style="red")
                return 

        elif len(command_list) > 1:
            first_argu = remove_commas(
                command_list[1]).lower()

            if first_argu == "json":
                # call that such specific method (function) according to given command
                action(json_result=True)
                return True
            else:
                console.print(
                    "Please use valid argument \"json\" in order to get JSON format response.\n", style="red")
                return 

        else:
            # call that such specific method (function) according to given command
            action() 
            
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

                # to check elasticsearch cluster health -------------------------------
                elif user_input.lower().startswith("health"):
                    health_check_cmd = user_input.split()

                    if len(health_check_cmd) > 1:
                        if health_check_cmd[1].lower() not in {"true", "false"}:
                            console.print(
                                "Please use valid argument \"true\" or \"false\" in order to get AI-powered summary\n", style="red")
                            continue

                        elif health_check_cmd[1].lower() == "true":
                            coreops.check_cluster_health(True)

                        else:
                            coreops.check_cluster_health()

                    else:
                        coreops.check_cluster_health()

                # to see list of existing shards ---------------------------------------
                elif user_input.lower().startswith("shards"):
                    double_argu_command_handler(user_input, coreops.available_shards)

                # to see list of existing indices ------------------------------------------
                elif user_input.lower().startswith("indices"):
                    double_argu_command_handler(user_input, coreops.list_indices)

                # to ping to cluster to check health ----------------------------------------
                elif user_input.lower() == "ping":
                    coreops.ping()

                # to see specific existing index details ---------------------------------------
                elif user_input.lower().startswith("indexinfo"):
                    double_argu_command_handler(user_input, coreops.index_details)

                # to see master nodes --------------------------------
                elif user_input.lower() == "master":
                    cmd_to_see_master_node = user_input.split()

                    if len(cmd_to_see_master_node) > 1:
                        argu = remove_commas(cmd_to_see_master_node).lower()

                        if argu == "json":
                            coreops.master_node(json_result=True)
                        else:
                            console.print(
                                "Please use valid argument \"json\" in order to get JSON format response.\n", style="red")
                            continue
                    else:
                        coreops.active_nodes()

                # see list of active nodes -------------------------------
                elif user_input.lower().startswith("nodes"):
                    double_argu_command_handler(user_input, coreops.active_nodes)

                # see storage capacities of active nodes ---------------------------------
                elif user_input.lower().startswith("capacity"):
                    double_argu_command_handler(user_input, coreops.nodes_capacity)

                # update or add new elasticsearch base url
                elif user_input.lower().startswith("conn"):
                    command_to_updated_elastic_base_url = user_input.split()
                    if len(command_to_updated_elastic_base_url) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"conn <base_url>\" to add or updated with new Elasticsearch base request URL.\n", style="red")
                        continue

                    coreops.new_password(remove_commas(
                        command_to_updated_elastic_base_url[1]))

                # update or add new elasticsearch password for connection
                elif user_input.lower().startswith("newcred"):
                    command_to_update_elastic_password = user_input.split()
                    if len(command_to_update_elastic_password) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"newcred <new_password>\" to add or updated elastic password for connection.\n", style="red")
                        continue

                    coreops.new_password(remove_commas(
                        command_to_update_elastic_password[1]))

                # clear console
                elif user_input.lower() in ("clear", "cls"):
                    print("\033[2J\033[H")

                # ----------------------------------------------------------------------
                #                       CRUD Commands handling
                # ----------------------------------------------------------------------

                # to create a new index
                elif user_input.lower().startswith("index:new"):
                    command_to_create_new_index = user_input.split()
                    if len(command_to_create_new_index) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"index:new <index_name>\" to create a new index.\n", style="red")
                        continue

                    crudops.new_index(remove_commas(
                        command_to_create_new_index[1]))

                # to delete a existing index
                elif user_input.lower().startswith("index:del"):
                    command_to_delete_index = user_input.split()
                    if len(command_to_delete_index) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"index:del <index_name>\" to delete a existing index.\n", style="red")
                        continue

                    crudops.del_index(remove_commas(
                        command_to_delete_index[1]))

                # to insert document into existing index
                elif user_input.lower().startswith("addoc"):
                    command_to_insert_document = user_input.split()
                    if len(command_to_insert_document) < 3:
                        console.print(
                            "[!] Please use the correct syntax of command \"addoc <index_name> <document_in_str>\" to add document into existing index.\n", style="red")
                        continue

                    # extract document fields and values and build a proper document string
                    doc_str = ""
                    for i in command_to_insert_document[2:]:
                        if i == command_to_insert_document[-1]:
                            doc_str += i
                            break
                        else:
                            doc_str += i
                            doc_str += " "

                    crudops.add_doc(remove_commas(
                        command_to_insert_document[1]), doc_str)

                # to see specific document
                elif user_input.lower().startswith("inspect:doc"):
                    command_to_see_specific_doc = user_input.split()
                    if len(command_to_see_specific_doc) < 3:
                        console.print(
                            "[!] Please use the correct syntax of command \"inspect:doc <index_name> <document_id>\" to see a specific document.\n", style="red")
                        continue

                    crudops.see_specific_doc(remove_commas(
                        command_to_see_specific_doc[1]), remove_commas(command_to_see_specific_doc[2]))

                # to see specific index stored data (inspect stored data)
                elif user_input.lower().startswith("inspect:index"):
                    command_to_see_specific_index = user_input.split()
                    if len(command_to_see_specific_index) < 2:
                        console.print(
                            "[!] Please use the correct syntax of command \"inspect:index <index_name> <no. of documents to see>\" to inspect specific index to see stored data (documents).\n", style="red")
                        continue

                    crudops.inspect_index_data(remove_commas(
                        command_to_see_specific_index[1]))

                # to update existing document in any specific index
                elif user_input.lower().startswith("updoc"):
                    command_to_update_doc = user_input.split()
                    if len(command_to_update_doc) < 4:
                        console.print(
                            "[!] Please use the correct syntax of command \"updoc <index_name> <document_id> <document_in_str>\" to update document into existing index.\n", style="red")
                        continue

                    # extract document fields and values and build a proper document string
                    doc_str = ""
                    for i in command_to_update_doc[3:]:
                        if i == command_to_update_doc[-1]:
                            doc_str += i
                            break
                        else:
                            doc_str += i
                            doc_str += " "

                    crudops.update_doc(remove_commas(command_to_update_doc[1]), remove_commas(
                        command_to_update_doc[2]),  doc_str)

                elif user_input.lower() in ("exit", "quit", "q", "ex"):
                    console.print("See ya!", style="bold")
                    sys.exit(0)

            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)

    except Exception as e:
        console.print(e, style="bold red")
