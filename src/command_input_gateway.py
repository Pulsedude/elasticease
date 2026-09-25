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

    def ping_command_handler(self, command: str = None):
        """Special command handler to ping cluster to check health"""
        coreops.ping()

    def indexinfo_command_handler(self, command: str):
        """Special command handler to see specific existing index details"""
        cmd_to_see_index_details = command.split()

        if len(cmd_to_see_index_details) > 2:
            first_argu = remove_commas(
                cmd_to_see_index_details[2])

            if first_argu.lower() == "true":
                coreops.index_details(ai_summarization=True)
                return
            else:
                console.print(
                    "Please use valid argument \"true\" or \"false\" in order to get AI-powered summary. Or use command \"help indexinfo\" to see exact usage of command with available optional arguments.\n", style="red")
                return

        elif len(cmd_to_see_index_details) > 1:
            index_name = remove_commas(
                cmd_to_see_index_details[1])
            coreops.index_details(index_name)
            return

        else:
            console.print(
                f"[!] You: {command}\nPlease provide a at least one required argument [index_name]. Or use command \"help indexinfo\" to see exact usage of command with available optional arguments.\n", style="red")
            return

    def master_command_handler(self, command: str):
        """Special command handler to see master nodes"""
        cmd_to_see_master_node = command.split()

        if len(cmd_to_see_master_node) > 1:
            argu = remove_commas(
                cmd_to_see_master_node).lower()

            if argu == "json":
                coreops.master_node(json_result=True)
            else:
                console.print(
                    "Please use valid argument \"json\" in order to get JSON format response. Or use command \"help master\" to see exact usage of command with available optional arguments.\n", style="red")
                return
        else:
            coreops.active_nodes()

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
        command_to_updated_elastic_base_url = command.split()
        
        if len(command_to_updated_elastic_base_url) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"conn <base_url>\" to add or updated with new Elasticsearch base request URL. Or use command \"help conn\" to see exact usage of command.\n", style="red")
            return

        coreops.new_password(remove_commas(
            command_to_updated_elastic_base_url[1]))

    def newcred_command_handler(self, command: str):
        """Special command handler to update or add new elasticsearch password for connection"""
        command_to_update_elastic_password = command.split()
        
        if len(command_to_update_elastic_password) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"newcred <new_password>\" to add or updated elastic password for connection. Or use command \"help newcred\" to see exact usage of command.\n", style="red")
            return

        coreops.new_password(remove_commas(
            command_to_update_elastic_password[1]))

    def clear_command_handler(self):
        """Special command handler to clear console"""
        print("\033[2J\033[H")

    # ----------------------------------------------------------------------
    #                       CRUD Command Handlers
    # ----------------------------------------------------------------------

    def new_index_command_handler(self, command: str):
        """Special command handler to create a new index"""
        command_to_create_new_index = command.split()

        if len(command_to_create_new_index) > 2:
            arg1, arg2 = remove_commas(command_to_create_new_index[1]), remove_commas(command_to_create_new_index[2])
            
            if arg2 not in {"true", "false"}:
                console.print(f"[!] You: {command}\nIf you want to provide your own custom mappings then please use \"true\" for it else leave empty or use \"false\". Or use command \"help index:new\" to see exact usage of command with optional arguments.\n", style="red")
                return
            
            if arg2.lower() == "true":
                crudops.new_index(arg1, True)
                return
            else:
                crudops.new_index(arg1)
                return

        elif len(command_to_create_new_index) > 1:
            arg1 = remove_commas(command_to_create_new_index[1])
            crudops.new_index(arg1)
            return

        else:
            console.print(
                f"[!] You: {command}\nPlease use the correct syntax of command \"index:new <index_name>\" to create a new index without custom mappings. If you want a custom mappings then use syntax \"index:new \"stundents\" \"name: text, age: integer, address: text, email: keyword\"\". Or use command \"help index:new\" to see exact usage of command with optional arguments.\n", style="red")
            return

    def index_del_command_handler(self, command: str):
        """Special command handler to delete an existing index"""
        command_to_delete_index = command.split()
        
        if len(command_to_delete_index) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"index:del <index_name>\" to delete a existing index. Or use command \"help index:del\" to see exact usage of command.\n", style="red")
            return

        crudops.del_index(remove_commas(
            command_to_delete_index[1]))

    def addoc_command_handler(self, command: str):
        """Special command handler to insert document into existing index"""
        command_to_insert_document = command.split()
        
        if len(command_to_insert_document) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"addoc <index_name> <document_in_str>\" to add document into existing index. Or use command \"help addoc\" to see exact usage of command.\n", style="red")
            return

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
        
        
    def addocs_command_handler(self, command: str):
        """Special command handler to insert multiple documents from single data (.json) file. Only supports .json file"""
        command_to_insert_documents = command.split()
        
        if len(command_to_insert_documents) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"addocs <index_name> <data_file_path>\" to add document into existing index. Or use command \"help addocs\" to exact usage of command.\n", style="red")
            return      

        index_name, data_file_path = remove_commas(command_to_insert_documents[1]), remove_commas(command_to_insert_documents[2])
        crudops.add_docs(index_name, data_file_path)
        

    def inspect_doc_command_handler(self, command: str):
        """Special command handler to see specific document"""
        command_to_see_specific_doc = command.split()
        
        if len(command_to_see_specific_doc) < 3:
            console.print(
                "[!] Please use the correct syntax of command \"inspect:doc <index_name> <document_id>\" to see a specific document. Or use command \"help inspect:doc\" to exact usage of command.\n", style="red")
            return

        crudops.see_specific_doc(remove_commas(
            command_to_see_specific_doc[1]), remove_commas(command_to_see_specific_doc[2]))

    def inspect_index_command_handler(self, command: str):
        """Special command handler to see specific index stored data (inspect stored data)"""
        command_to_see_specific_index = command.split()
        
        if len(command_to_see_specific_index) < 2:
            console.print(
                "[!] Please use the correct syntax of command \"inspect:index <index_name> <no. of documents to see>\" to inspect specific index to see stored data (documents). Or use command \"help inspect:index\" to exact usage of command.\n", style="red")
            return

        crudops.inspect_index_data(remove_commas(
            command_to_see_specific_index[1]))

    def updoc_command_handler(self, command: str):
        """Special command handler to update existing document in any specific index"""
        command_to_update_doc = command.split()
        if len(command_to_update_doc) < 4:
            console.print(
                "[!] Please use the correct syntax of command \"updoc <index_name> <document_id> <document_in_str>\" to update document into existing index. Or use command \"help updoc\" to see exact usage of command.\n", style="red")
            return

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
                    elif user_input.lower() == "ping":
                        self.ping_command_handler(user_input)

                    # to see specific existing index details ---------------------------------------
                    elif user_input.lower().startswith("indexinfo"):
                        self.indexinfo_command_handler(user_input)

                    # to see master nodes --------------------------------
                    elif user_input.lower() == "master":
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

                    # update or add new elasticsearch password for connection
                    elif user_input.lower().startswith("newcred"):
                        self.newcred_command_handler(user_input)

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

                    # to insert multiple documents from single data file (.json) to existing index
                    elif user_input.lower().startswith("addocs"):
                        
                        self.addocs_command_handler(user_input)
                    # to insert document into existing index
                    elif user_input.lower().startswith("addoc"):
                        self.addoc_command_handler(user_input)
                        

                    # to see specific document
                    elif user_input.lower().startswith("inspect:doc"):
                        self.inspect_doc_command_handler(user_input)

                    # to see specific index stored data (inspect stored data)
                    elif user_input.lower().startswith("inspect:index"):
                        self.inspect_index_command_handler(user_input)

                    # to update existing document in any specific index
                    elif user_input.lower().startswith("updoc"):
                        self.updoc_command_handler(user_input)

                    elif user_input.lower() in ("exit", "quit", "q", "ex"):
                        self.exit_command_handler()

                except KeyboardInterrupt:
                    console.print("See ya!", style="bold")
                    sys.exit(1)

        except Exception as e:
            console.print(e, style="bold red")
