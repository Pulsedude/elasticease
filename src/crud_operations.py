from rich.console import Console
from rich.json import JSON
from .config import read
import requests
import json
import sys

# utils
from .utils import create_document

console = Console()

class CrudOps:
    def __init__(self):
        self.configuration = read()["elasticease"]
        self.auth = (self.configuration["username"], self.configuration["password"])
        self.base_url = self.configuration["base_url"]
        
    def create_new_index(self, index_name: str):
        """Create new index
        """
        try:
            try:
                response = requests.put(
                    self.base_url + f"/{index_name}" if not self.base_url.endswith("/") else self.base_url + index_name,
                    timeout=10,
                    auth=self.auth,
                    verify=False
                )
                
                if response.raise_for_status():
                    console.print(f"[!] Something went wrong! Please check the base url and try again\n", style="red")
                    return
                
                console.print(JSON(json.dumps(response.json())))
                print()
                
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
        except Exception as e:
            console.print(e, style="bold red")
            print()
        
    def delete_index(self, index_name: str):
        """Delete any specific existing index
        """
        try:
            try:
                response = requests.delete(
                    self.base_url + f"/{index_name}" if not self.base_url.endswith("/") else self.base_url + index_name,
                    timeout=10,
                    auth=self.auth,
                    verify=False
                ) 
                
                if response.raise_for_status():
                    console.print(f"[!] Something went wrong! Please check the base url and try again\n", style="red")
                    return
                
                console.print(JSON(json.dumps(response.json())))
                print()
                
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
        except Exception as e:
            console.print(e, style="bold red")
            print()
            
    
    def add_document(self, index_name: str, document_str: str):
        """Insert a document into specific existing index
        """
        try:
            try:
                document = create_document(document_str)
                response = requests.post(
                    self.base_url + f"/{index_name}/_doc" if not self.base_url.endswith("/") else self.base_url + f"{index_name}/_doc",
                    json=document,
                    timeout=10,
                    auth=self.auth,
                    verify=False
                ) 
                
                if response.raise_for_status():
                    console.print(f"[!] Something went wrong! Please check the base url and try again\n", style="red")
                    return
                
                console.print(JSON(json.dumps(response.json())))
                print()
                
                
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
        except Exception as e:
            console.print(e, style="bold red")
            print()
            
    def see_specific_document(self, index_name: str, document_id: str):
        """See specific document from any existing index
        """
        try:
            try:
                response = requests.get(
                    self.base_url + f"/{index_name}/_doc/{document_id}" if not self.base_url.endswith("/") else self.base_url + f"{index_name}/_doc/{document_id}",
                    timeout=10,
                    auth=self.auth,
                    verify=False
                ) 
                
                if response.raise_for_status():
                    console.print(f"[!] Something went wrong! Please check the base url and try again\n", style="red")
                    return
                
                console.print(JSON(json.dumps(response.json())))
                print()
                
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
        except Exception as e:
            console.print(e, style="bold red")
            print()
            
            
    def see_specific_index(self, index_name: str):
        """See specific index with their stored data
        """
        try:
            try:
                query = {
                    "query": {
                        "match_all": {}
                    }
                }
                response = requests.get(
                    self.base_url + f"/{index_name}/_search" if not self.base_url.endswith("/") else self.base_url +f"{index_name}/_search/",
                    json=query,
                    timeout=10,
                    auth=self.auth,
                    verify=False
                ) 
                
                if response.raise_for_status():
                    console.print(f"[!] Something went wrong! Please check the base url and try again\n", style="red")
                    return
                
                console.print(JSON(json.dumps(response.json())))
                print()
                
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
        except Exception as e:
            console.print(e, style="bold red")
            print()
    
    def update_document(self, index_name: str, document_id: str, document_str: str):
        """Insert a document into specific existing index
        """
        try:
            try:
                document = {
                    "doc": create_document(document_str)
                }
                response = requests.put(
                    self.base_url + f"/{index_name}/_doc/{document_id}" if not self.base_url.endswith("/") else self.base_url + f"{index_name}/_doc/{document_id}",
                    json=document,
                    timeout=10,
                    auth=self.auth,
                    verify=False
                )
                
                if response.raise_for_status():
                    console.print(f"[!] Something went wrong! Please check the base url and try again\n", style="red")
                    return
                
                console.print(JSON(json.dumps(response.json())))
                print()
                
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
        except Exception as e:
            console.print(e, style="bold red")
            print()
    
    
