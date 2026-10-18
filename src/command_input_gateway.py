from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
import sys

# util functions
from .utils import remove_commas

# core operaitons  ------
from .core_operations import CoreOps

# crud operaitons ------
from .crud_operations import CrudOps

# available commands ------
from .commands import core_commands, crud_commands

console = Console()
coreops = CoreOps()
crudops = CrudOps()


class CommandInputGateway:

    def core_commands_double_argu_handler(self, command: str, action):
        """Special command handler for commands which supports double arguments (json, AI Summarization)
        """
        command_list = command.split()

        # for command passed with double arguments
        if len(command_list) > 2:
            first_argu = remove_commas(
                command_list[1]).lower()
            sec_argu = remove_commas(
                command_list[2]).lower()
            passed_args = []  # storing passed argument for validation

            # check second argument
            passed_args.append(first_argu)
            passed_args.append(sec_argu)

            # arguments validation
            if passed_args[0] == passed_args[1]:
                console.print(f"[!] You: {command}\nYou are passing same parameters for both arguments. Please use to correct it and use to pass right parameters for specific argument, use [\"json\"] to get response in JSON format and use [\"true\" or \"false\"] to get AI-powered summary. Or use command \"help {command[0]}\" to exact usage of command with available optional arguments.\n", style="red")
                return

            sorted_args = sorted(passed_args)
            print(sorted_args)

            if sorted_args == ["json", "true"] or sorted_args == ["false", "json"]:
                action(json_result=True, ai_summarization=True)
                return

            else:
                console.print(f"[!] You: {command}\nThis command supports two special arguments 1st argument for json results if you want response in JSON format and 2nd argument for AI-powered data summarization you want a proper data summary. So please use pass correct argument you are allowed to use any such argument from [\"json\"] for json result flag and [\"true\" or \"false\"] for AI-powered summary flag. Pass in any such order but pass with as correct parameter. Or use command \"help {command[0]}\" to exact usage of command with available optional arguments.\n", style="red")
                return

        # command passed with single argument
        elif len(command_list) > 1:
            first_argu = remove_commas(
                command_list[1]).lower()

            if first_argu == "json":
                action(json_result=True)
                return

            elif first_argu == "true":
                action(ai_summarization=True)
                return

            elif first_argu == "false":
                action(ai_summarization=False)
                return
            else:
                console.print(f"[!] You: {command}\nPlease use correct paramters to pass in arguments if you are passing single argument with command which supports two special arguments one for json results to get response in proper JSON format and 2nd for AI-powered summary to get AI-powered summary on specific data. So you can you use [\"json\"] to get response in JSON format or [\"true\" or \"false\"] for AI-powered summarization. Or use command \"help {command[0]}\" to exact usage of command with available optional arguments.\n", style="red")
                return

        else:
            action()

    # ----------------------------------------------------------------------
    #                       Core Command Handlers
    # ----------------------------------------------------------------------

    def health_command_handler(self, command: str):
        """Special command handler to check elasticsearch cluster health"""
        health_check_cmd = command.split()

        if len(health_check_cmd) > 1:
            if health_check_cmd[1].lower() not in {"true", "false"}:
                console.print(
                    "Please use valid argument \"true\" or \"false\" in order to get AI-powered summary. Or use command \"help heatlh\" to see exact usage of command with available optional arguments.\n", style="red")
                return

            elif health_check_cmd[1].lower() == "true":
                coreops.check_cluster_health(True)

            else:
                coreops.check_cluster_health()

        else:
            coreops.check_cluster_health()

    def shards_command_handler(self, command: str):
        """Special command handler to see list of existing shards"""
        self.core_commands_double_argu_handler(
            command, coreops.available_shards)

    def indices_command_handler(self, command: str):
        """Special command handler to see list of existing indices"""
        self.core_commands_double_argu_handler(
            command, coreops.list_indices)

    def ping_command_handler(self, command: str = "ping"):
        """Special command handler to ping cluster to check health"""
        ping_command = command.split()
        if len(ping_command) > 1 and ping_command[1].lower() == "true":
            coreops.ping(ai_summarization=True)
        else:
            coreops.ping()

    def indexinfo_command_handler(self, command: str):
        """Special command handler to see specific existing index details"""
        indexinfo_command = command.split()

        if len(indexinfo_command) > 2:
            index_name = remove_commas(indexinfo_command[1])
            first_argu = remove_commas(
                indexinfo_command[2])

            if first_argu.lower() == "true":
                coreops.index_details(index_name, ai_summarization=True)
                return
            else:
                console.print(
                    "Please use valid argument \"true\" or \"false\" in order to get AI-powered summary. Or use command \"help indexinfo\" to see exact usage of command with available optional arguments.\n", style="red")
                return

        elif len(indexinfo_command) > 1:
            index_name = remove_commas(
                indexinfo_command[1])
            coreops.index_details(index_name)
            return

        else:
            console.print(
                f"[!] You: {command}\nPlease provide a at least one required argument [index_name]. Or use command \"help indexinfo\" to see exact usage of command with available optional arguments.\n", style="red")
            return

    def master_command_handler(self, command: str):
        """Special command handler to see master nodes"""
        master_inspect_command = command.split()

        if len(master_inspect_command) > 1:
            argu = remove_commas(
                master_inspect_command[1]).lower()

            if argu == "json":
                coreops.master_node(json_result=True)
            else:
                console.print(
                    "Please use valid argument \"json\" in order to get JSON format response. Or use command \"help master\" to see exact usage of command with available optional arguments.\n", style="red")
                return
        else:
            coreops.master_node()

    def nodes_command_handler(self, command: str):
        """Special command handler to see list of active nodes"""
        self.core_commands_double_argu_handler(
            command, coreops.active_nodes)

    def capacity_command_handler(self, command: str):
        """Special command handler to see storage capacities of active nodes"""
        self.core_commands_double_argu_handler(
            command, coreops.nodes_capacity)

    def conn_command_handler(self, command: str):
        """Special command handler to update or add new elasticsearch base url"""
        conn_command = command.split()

        if len(conn_command) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"conn <base_url>\" to add or updated with new Elasticsearch base request URL. Or use command \"help conn\" to see exact usage of command.\n", style="red")
            return

        coreops.new_base_url(remove_commas(
            conn_command[1]))

    def ainf_command_handler(self, command: str):
        """Special command handler to handle command ainf to switch to another available Ai-Inference (provider) or see active one"""
        ainf_command = command.split()

        if len(ainf_command) > 1:
            arg2 = ainf_command[1].lower()

            if arg2 == "switch":
                coreops.switch_ai_inference()
                return
            else:
                console.print(
                    "[!] Please use the correct syntax of command \"ainf\" to see selected & active AI-Inference (provider) or switch to another one. Or use command \"help ainf\" to see exact usage of command.\n", style="red")
                return
        else:
            coreops.active_ai_inference()

    def newcred_command_handler(self, command: str):
        """Special command handler to update or add new elasticsearch password for connection"""
        newcred_command = command.split()

        if len(newcred_command) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"newcred <new_password>\" to add or updated elastic password for connection. Or use command \"help newcred\" to see exact usage of command.\n", style="red")
            return

        coreops.new_password(remove_commas(
            newcred_command[1]))

    def help_command_handler(self, command: str):
        """Command handler to handle help command
        """
        help_command = command.split()

        if len(help_command) > 2:
            console.print(
                "[!] help command does not support more than two arguments\n", style="red")
            return

        elif len(help_command) == 2:
            command_name = remove_commas(help_command[1]).lower()

            for options in [core_commands, crud_commands]:
                for option in options:
                    if option.get("name") == command_name or option.get("name").split()[0] == command_name or (command_name in ("newcred", "newpass") and option.get("name").startswith("newpass")) or (command_name in ("clear", "cls") and option.get("name") == "clear"):
                        
                        name = option.get("name")
                        required_arguments = option.get("arguments").get(
                            "required") if option.get("arguments") else None
                        optional_arguments = option.get("arguments").get(
                            "optional") if option.get("arguments") else None
                        purpose = option.get("purpose")
                        example = option.get("example")
                        info = option.get("info")
                        req_args = f"`{required_arguments}`" if required_arguments else "None"
                        opt_args = f"`{optional_arguments}`" if optional_arguments else "None"
                        ex_str = f"`{example}`" if example else "None"
                        purpose_str = purpose if purpose else "None"

                        info_lines = [line.strip() for line in info.strip(
                        ).splitlines() if line.strip()] if info else []
                        info_str = "  \n  ".join(
                            info_lines) if info_lines else "None"

                        command_md = f"""
# Command: `{name}`
- **Purpose:** {purpose_str}
- **Required Arguments:** {req_args}
- **Optional Arguments:** {opt_args}
- **Example:** {ex_str}
- **Info:**  
  {info_str}
---
"""
                        console.print(Markdown(command_md))
                        return

            console.print(
                f"[!] command with name \"{command_name}\" not found!\n", style="red")
            return

        else:
            for idx, options in enumerate([core_commands, crud_commands]):
                console.print("=" * 37, style="cyan")

                if idx > 0:
                    console.print("Available options for CRUD operations")
                else:
                    console.print("Available options for Core operations")

                console.print("=" * 37, style="cyan")
                print()

                for option in options:
                    name = option.get("name")
                    required_arguments = option.get(
                        "arguments").get("required")
                    optional_arguments = option.get(
                        "arguments").get("optional")
                    purpose = option.get("purpose")
                    example = option.get("example")
                    info = option.get("info")
                    req_args = f"`{required_arguments}`" if required_arguments else "None"
                    opt_args = f"`{optional_arguments}`" if optional_arguments else "None"
                    ex_str = f"`{example}`" if example else "None"
                    purpose_str = purpose if purpose else "None"

                    info_lines = [line.strip() for line in info.strip(
                    ).splitlines() if line.strip()] if info else []
                    info_str = "  \n  ".join(
                        info_lines) if info_lines else "None"

                    command_md = f"""
### Command: `{name}`
- **Purpose:** {purpose_str}
- **Required Arguments:** {req_args}
- **Optional Arguments:** {opt_args}
- **Example:** {ex_str}
- **Info:**  
  {info_str}
---
"""
                    console.print(Markdown(command_md))

    def clear_command_handler(self):
        """Special command handler to clear console"""
        print("\033[2J\033[H")

    # ----------------------------------------------------------------------
    #                       CRUD Command Handlers
    # ----------------------------------------------------------------------

    def new_index_command_handler(self, command: str):
        """Special command handler to create a new index"""
        index_new_command = command.split()

        if len(index_new_command) > 2:
            arg1, arg2 = remove_commas(index_new_command[1]), remove_commas(
                index_new_command[2]).lower()
            if arg2 != "mappings":
                console.print(
                    f"[!] You: {command}\nIf you want to provide your own custom mappings then please use \"mappings\" for it else leave empty. Or use command \"help index:new\" to see exact usage of command with optional arguments.\n", style="red")
                return

            if arg2.lower() == "mappings":
                crudops.new_index(arg1, custom_mappings=True)
                return
            else:
                crudops.new_index(arg1)
                return

        elif len(index_new_command) > 1:
            arg1 = remove_commas(index_new_command[1])
            crudops.new_index(arg1)
            return

        else:
            console.print(
                f"[!] You: {command}\nPlease use the correct syntax of command \"index:new <index_name>\" to create a new index without custom mappings. If you want a custom mappings then use syntax \"index:new \"stundents\" \"name: text, age: integer, address: text, email: keyword\"\". Or use command \"help index:new\" to see exact usage of command with optional arguments.\n", style="red")
            return

    def index_del_command_handler(self, command: str):
        """Special command handler to delete an existing index"""
        index_del_command = command.split()

        if len(index_del_command) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"index:del <index_name>\" to delete a existing index. Or use command \"help index:del\" to see exact usage of command.\n", style="red")
            return

        crudops.del_index(remove_commas(
            index_del_command[1]))

    def addoc_command_handler(self, command: str):
        """Special command handler to insert document into existing index"""
        addoc_command = command.split()

        if len(addoc_command) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"addoc <index_name> <key_values>\" to add document into existing index. Or use command \"help addoc\" to see exact usage of command.\n", style="red")
            return

        # extract document fields and values and build a proper document string
        doc_str = ""
        for i in addoc_command[2:]:
            if i == addoc_command[-1]:
                doc_str += i
                break
            else:
                doc_str += i
                doc_str += " "

        crudops.add_doc(remove_commas(
            addoc_command[1]), doc_str)

    def addocs_command_handler(self, command: str):
        """Special command handler to insert multiple documents from single data (.json) file. Only supports .json file"""
        addocs_command = command.split()

        if len(addocs_command) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"addocs <index_name> <data_file_path>\" to add document into existing index. Or use command \"help addocs\" to exact usage of command.\n", style="red")
            return

        index_name = remove_commas(addocs_command[1])
        data_file_path = remove_commas(" ".join(addocs_command[2:]))
        crudops.add_docs(index_name, data_file_path)

    def inspect_doc_command_handler(self, command: str):
        """Special command handler to see specific document"""
        inspect_do_command = command.split()

        if len(inspect_do_command) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"inspect:doc <index_name> <document_id>\" to see a specific document. Or use command \"help inspect:doc\" to exact usage of command.\n", style="red")
            return

        crudops.see_specific_doc(remove_commas(
            inspect_do_command[1]), remove_commas(inspect_do_command[2]))

    def inspect_index_command_handler(self, command: str):
        """Special command handler to see specific index stored data (inspect stored data)"""
        inspect_index_command = command.split()

        if len(inspect_index_command) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"inspect:index <index_name> <no. of documents to see>\" to inspect specific index to see stored data (documents). Or use command \"help inspect:index\" to exact usage of command.\n", style="red")
            return

        crudops.inspect_index_data(remove_commas(
            inspect_index_command[1]))

    def updocs_command_handler(self, command: str):
        """Special command handler to update multiple existing documents at once. Need supported data file (.json) in which having data and according to data updation operation will performed"""
        updocs_command = command.split()

        if len(updocs_command) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"updocs <index_name> <data_file_path>\" to update multiple documents at once into existing index. Or use command \"help updocs\" to see exact usage of command.\n", style="red")
            return

        index_name = remove_commas(updocs_command[1])
        data_file_path = remove_commas("".join(updocs_command[2:]))
        crudops.update_docs(index_name, data_file_path)

    def updoc_command_handler(self, command: str):
        """Special command handler to update existing document in any specific index"""
        updoc_command = command.split()
        if len(updoc_command) < 4:
            console.print(
                "[!] Please use the correct syntax of command \"updoc <index_name> <document_id> <document_in_str>\" to update document into existing index. Or use command \"help updoc\" to see exact usage of command.\n", style="red")
            return

        # extract document fields and values and build a proper document string
        doc_str = ""
        for i in updoc_command[3:]:
            if i == updoc_command[-1]:
                doc_str += i
                break
            else:
                doc_str += i
                doc_str += " "

        crudops.update_doc(remove_commas(updoc_command[1]), remove_commas(
            updoc_command[2]),  doc_str)

    def deldoc_command_handler(self, command: str):
        """Special command handler to delete any such particular document
        """
        deldoc_command = command.split()
        if len(deldoc_command) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"deldoc <index_name> <document_id>\" to delete single document. Or use command \"help deldoc\" to see exact usage of command.\n", style="red")
            return

        crudops.delete_doc(remove_commas(
            deldoc_command[1]), remove_commas(deldoc_command[2]))

    def deldocs_command_handler(self, command: str):
        """Special command handler to delete any such particular document
        """
        dedocs_command = command.split()
        if len(dedocs_command) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"deldocs <index_name> <targets>\" to delete single document. Or use command \"help deldocs\" to see exact usage of command.\n", style="red")
            return

        crudops.delete_docs(remove_commas(
            dedocs_command[1]), remove_commas(dedocs_command[2]))

    def exit_command_handler(self):
        """Special command handler to exit elasticease"""
        console.print("See ya!", style="bold")
        sys.exit(0)

    def user_input_loop(self):
        """User input (command) loop & handler to allow user to perform various operations through available commands
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

                    # to check elasticsearch cluster health -------------------------------
                    elif user_input.lower().startswith("health"):
                        self.health_command_handler(user_input)

                    # to see list of existing shards ---------------------------------------
                    elif user_input.lower().startswith("shards"):
                        self.shards_command_handler(user_input)

                    # to see list of existing indices ------------------------------------------
                    elif user_input.lower().startswith("indices"):
                        self.indices_command_handler(user_input)

                    # to ping to cluster to check health ----------------------------------------
                    elif user_input.lower().startswith("ping"):
                        self.ping_command_handler(user_input)

                    # to see specific existing index details ---------------------------------------
                    elif user_input.lower().startswith("indexinfo"):
                        self.indexinfo_command_handler(user_input)

                    # to see master nodes --------------------------------
                    elif user_input.lower().startswith("master"):
                        self.master_command_handler(user_input)

                    # see list of active nodes -------------------------------
                    elif user_input.lower().startswith("nodes"):
                        self.nodes_command_handler(user_input)

                    # see storage capacities of active nodes ---------------------------------
                    elif user_input.lower().startswith("capacity"):
                        self.capacity_command_handler(user_input)

                    # update or add new elasticsearch base url
                    elif user_input.lower().startswith("conn"):
                        self.conn_command_handler(user_input)

                    # see active & selected AI-Inference (provider) and also switch to another available one
                    elif user_input.lower().startswith("ainf"):
                        self.ainf_command_handler(user_input)

                    # update or add new elasticsearch password for connection
                    elif user_input.lower().startswith("newcred") or user_input.lower().startswith("newpass"):
                        self.newcred_command_handler(user_input)

                    # help command
                    elif user_input.lower().startswith("help"):
                        self.help_command_handler(user_input)

                    # clear console
                    elif user_input.lower() in ("clear", "cls"):
                        self.clear_command_handler()

                    # ----------------------------------------------------------------------
                    #                       CRUD Commands handling
                    # ----------------------------------------------------------------------

                    # to create a new index
                    elif user_input.lower().startswith("index:new"):
                        self.new_index_command_handler(user_input)

                    # to delete a existing index
                    elif user_input.lower().startswith("index:del"):
                        self.index_del_command_handler(user_input)

                    # to see specific document
                    elif user_input.lower().startswith("inspect:doc"):
                        self.inspect_doc_command_handler(user_input)

                    # to see specific index stored data (inspect stored data)
                    elif user_input.lower().startswith("inspect:index"):
                        self.inspect_index_command_handler(user_input)

                    # to insert multiple documents from single data file (.json) to existing index
                    elif user_input.lower().startswith("addocs"):
                        self.addocs_command_handler(user_input)

                    # to insert document into existing index
                    elif user_input.lower().startswith("addoc"):
                        self.addoc_command_handler(user_input)

                    # to update multiple existing documents at once
                    elif user_input.lower().startswith("updocs"):
                        self.updocs_command_handler(user_input)

                    # to update single existing document
                    elif user_input.lower().startswith("updoc"):
                        self.updoc_command_handler(user_input)

                    # to delete multiple existing documents at once
                    elif user_input.lower().startswith("deldocs"):
                        self.deldocs_command_handler(user_input)

                    # to delete single existing document
                    elif user_input.lower().startswith("deldoc"):
                        self.deldoc_command_handler(user_input)

                    elif user_input.lower() in ("exit", "quit", "q", "ex"):
                        self.exit_command_handler()

                except KeyboardInterrupt:
                    console.print("See ya!", style="bold")
                    sys.exit(1)

        except Exception as e:
            console.print(e, style="bold red")
