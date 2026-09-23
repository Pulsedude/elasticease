from rich.console import Console
from rich.prompt import Prompt
from rich.json import JSON
from .config import read
import json
import asyncio

# custom request logic
from .request import Request

# utilites
from .utils import create_document, create_mappings

console = Console()
req = Request()


class CrudOps:
    def __init__(self):
        self.configuration = read().get("elasticease")

    def new_index(self, index_name: str, custom_mappings: bool = False, mappings: dict = {}):
        """Create new index
        """
        try:
            if not custom_mappings:
                response = asyncio.run(req.put(index_name))

                if isinstance(response, tuple):
                    console.print(response[1], style="bold red")
                    print()
                    return

                console.print(JSON(json.dumps(response.get("response"))))
                print()
                return

            else:
                mappings = {}

                # input from user to create custom mapping
                console.print(
                    "\nPlease enter the fields that you want for your index:\nProvide just like that - e.g. \"name: text, age: integer, addres: text, about: text\n", style="bold")
                while True:
                    user = input("> ")

                    if not user:
                        continue

                    else:
                        # confirmation input
                        while True:
                            confirmation = Prompt.ask(
                                "\nPlease recheck your provided mappings:\nconfirm [green][Y][green]/[red][N][red]")

                            if not confirmation:
                                continue
                            
                            if confirmation.lower() in {"no", "n"}:
                                continue
                            
                            else:
                                break

                        mappings = create_mappings(user)
                        break

                response = asyncio.run(req.put(index_name, mappings))

                if isinstance(response, tuple):
                    console.print(response[1], style="bold red")
                    print()
                    return

                console.print(JSON(json.dumps(response.get("response"))))
                print()

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def del_index(self, index_name: str):
        """Delete any specific existing index
        """
        try:
            response = asyncio.run(req.delete(index_name))

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            console.print(JSON(json.dumps(response.get("response"))))
            print()

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def add_doc(self, index_name: str, document_str: str):
        """Insert a document into specific existing index
        """
        try:
            document = create_document(document_str)
            response = asyncio.run(req.post(index_name, document))

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            console.print(JSON(json.dumps(response.get("response"))))
            print()

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def see_specific_doc(self, index_name: str, document_id: str):
        """See specific document from any existing index
        """
        try:
            response = asyncio.run(req.get(f"{index_name}/_doc/{document_id}"))

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            console.print(JSON(json.dumps(response.get("response"))))
            print()

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def inspect_index_data(self, index_name: str, size: str = "100"):
        """See specific index with their stored data (inspect index)
        """
        try:

            response = asyncio.run(
                req.get(f"{index_name}/_search?size={size}"))

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            console.print(JSON(json.dumps(response.get("response"))))
            print()

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def update_doc(self, index_name: str, document_id: str, document_str: str):
        """Update existing index by following proper OCC (Optimistic Concurrency Control) rule
        """
        try:

            # first of all fetch the target document for their seq_no for checking whether document is modified or not to prevent from loss & update problem
            get_doc = asyncio.run(req.get(f"{index_name}/_doc/{document_id}"))

            if isinstance(get_doc, tuple):
                console.print(get_doc[1], style="bold red")
                print()
                return

            seq_no = get_doc.json()["_seq_no"]
            primary_term = get_doc.json()["_primary_term"]

            # update the document if _seq_no and _primary_term both are same (means no modification is made)
            document = {
                "doc": create_document(document_str)
            }
            updation_res = asyncio.run(req.put(
                f"{index_name}/_update/{document_id}?if_seq_no={seq_no}&if_primary_term={primary_term}", document))

            if isinstance(updation_res, tuple):
                console.print(updation_res[1], style="bold red")
                print()
                return

            console.print(JSON(json.dumps(updation_res.get("response"))))
            print()

        except Exception as e:
            console.print(e, style="bold red")
            print()
