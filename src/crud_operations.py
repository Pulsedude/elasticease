from rich.console import Console
from rich.json import JSON
from .config import read
import json
import sys

# custom request methods
from .request import get, post, put, delete

# utilites
from .utils import create_document

console = Console()


class CrudOps:
    def __init__(self):
        self.configuration = read().get("elasticease")

    def new_index(self, index_name: str):
        """Create new index
        """
        try:
            response = put(index_name)

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
            response = delete(index_name)

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
            response = post(index_name, document)

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
            response = get(f"{index_name}/_doc/{document_id}")

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
        """See specific index with their stored data
        """
        try:

            response = get(f"{index_name}/_search?size={size}")

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
        """Insert a document into specific existing index
        """
        try:

            # first of all fetch the target document for their seq_no for checking whether document is modified or not to prevent from loss & update problem
            get_doc = get(f"{index_name}/_doc/{document_id}")

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
            updation_res = put(
                f"{index_name}/_update/{document_id}?if_seq_no={seq_no}&if_primary_term={primary_term}", document)

            if isinstance(updation_res, tuple):
                console.print(updation_res[1], style="bold red")
                print()
                return

            console.print(JSON(json.dumps(updation_res.get("response"))))
            print()

        except Exception as e:
            console.print(e, style="bold red")
            print()
