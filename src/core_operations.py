from rich.console import Console
from .config import read, write
from rich.table import Table
import requests
import urllib3
import sys  

# disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

class CoreOps:
    def __init__(self):
        self.configuration = read()["elasticease"]
        self.auth = (self.configuration["username"], self.configuration["password"])
    
    def make_request(self, route: str = ""):
        """Make request to specific route on same base URL
        """
        try:
            try:
                response = requests.get(
                    url=self.configuration["base_url"] + f"/{route}" if not self.configuration["base_url"].endswith("/") else self.configuration["base_url"] + route,
                    timeout=10,
                    auth=self.auth,
                    verify=False
                )
            except KeyboardInterrupt:
                console.print("See ya!", style="bold")
                sys.exit(1)
                
            if response.status_code != 200:
                return False
            return response
        except Exception as e:
            return (False, e)
        
    def check_cluster_health(self):
        """Check a cluster health
        """
        try:
            cluster_health_info_table = Table(show_lines=True)
            response = self.make_request("_cluster/health").json()
            
            if not response:
                console.print(f"[!] {response.status_code}\nPlease check the base URL and make sure Elasticsearch is running on it", style="red")
                return
            
            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                return 
            
            cluster_health_info_table.add_column("[bright_yellow]Work[/bright_yellow]")
            cluster_health_info_table.add_column("[bright_cyan]Status[/bright_cyan]")

            for work, status in dict(response).items():
                cluster_health_info_table.add_row(
                    f"[bold]{work}[/bold]",
                    str(status)
                )
                
            console.print(cluster_health_info_table)
            print()
            
        except Exception as e:
            console.print(e, style="bold red")
    
    def available_shards(self):
        """See available shards
        """
        try:
            shards_table = Table(show_lines=True)
            
            response = self.make_request("_cat/shards?format=json").json()
            
            if not response:
                console.print(f"[!] {response.status_code}\nPlease check the base URL and make sure Elasticsearch is running on it", style="red")
                return

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                return
            
            # print(response)
            shards_table.add_column("index")
            shards_table.add_column("shard")
            shards_table.add_column("primary & replica")
            shards_table.add_column("state")
            shards_table.add_column("docs")
            shards_table.add_column("store")
            shards_table.add_column("dataset")
            shards_table.add_column("ip")
            shards_table.add_column("node")
            
            for shard_info in response:
                shards_table.add_row(
                    f"[bright_cyan]{shard_info.get("index")}[/bright_cyan]",
                    f"[bright_blue]{shard_info.get("shard")}[/bright_blue]",
                    f"[birght_yellow]{shard_info.get("prirep")}[/birght_yellow]",
                    f"[bright_green]{shard_info.get("state")}[/bright_green]",
                    f"[bright_magenta]{shard_info.get("docs")}[/bright_magenta]",
                    f"[turquoise2]{shard_info.get("store")}[/turquoise2]",
                    f"[blue_violet]{shard_info.get("dataset")}[/blue_violet]",
                    f"[light_cyan1]{shard_info.get("ip")}[/light_cyan1]",
                    f"[orange_red1]{shard_info.get("node")}[/orange_red1]",                    
                )
            
            console.print(shards_table)
            print()

        except Exception as e:
            console.print(e, style="bold red")

    def available_indices(self):
        """List all available indices
        """
        try:
            indices_table = Table(show_lines=True)
            response = self.make_request("_cat/indices?format=json").json()
            
            if not response:
                console.print(f"[!] {response.status_code}\nPlease check the base URL and make sure Elasticsearch is running on it", style="red")
                return

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                return
            
            indices_table.add_column("health")
            indices_table.add_column("status")
            indices_table.add_column("index")
            indices_table.add_column("uuid")
            indices_table.add_column("primary")
            indices_table.add_column("replica")
            indices_table.add_column("docs.count")
            indices_table.add_column("docs.deleted")
            indices_table.add_column("store.size")
            indices_table.add_column("pri.store.size")
            indices_table.add_column("dataset.size")
            
            for index_info in response:
                indices_table.add_row(
                    f"[bright_green]{index_info.get("health")}[/bright_green]" if index_info.get("health").lower() == "green" else f"[bright_yellow]{index_info.get("health")}[/bright_yellow]",
                    
                    f"[dark_turquoise]{index_info.get("status")}" if index_info.get("status").lower() == "open" else f"[orange3]{index_info.get("status")}[/orange3]",
                    
                    f"[bright_blue]{index_info.get("index")}[/bright_blue]",
                    
                    f"[white]{index_info.get("uuid")}[/white]",
                    
                    f"[spring_green2]{index_info.get("pri")}[/spring_green2]",
                    
                    f"[spring_green1]{index_info.get("rep")}[/spring_green1]",
                    
                    f"[purple]{index_info.get("docs.count")}[/purple]",
                    
                    f"[dark_khaki]{index_info.get("docs.deleted")}[/dark_khaki]",
                    
                    f"[light_sky_blue1]{index_info.get("store.size")}[/light_sky_blue1]",
                    
                    f"[light_cyan3]{index_info.get("pri.store.size")}[/light_cyan3]",
                    
                    f"[white]{index_info.get("dataset.size")}[/white]"
                )
            console.print(indices_table)
            print()
            
        except Exception as e:
            console.print(e, style="bold red")
        
    def ping(self):
        """Ping test on the cluster
        """
        try:
            response = self.make_request().json()
            
            if not response:
                console.print(f"[bold]Base URL:[/bold] [bright_blue]{self.configuration["base_url"]}[/bright_blue]\n[bold]Status:[/bold] ❌\n[!] Please check the base URL and make sure Elasticsearch is running on it", style="red")
                return

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                return
            
            console.print(f"[bold]Base URL:[/bold] [bright_blue]{self.configuration["base_url"]}[/bright_blue]\n[bold]Status:[/bold] 🟢 [bright_green]Healthy[/bright_green]\n")  
            console.print(response)     
            print()
             
        except Exception as e:
            console.print(e, style="bold red")
    
    def index_details(self, index_name: str, json: bool = False):
        """See details of specific target index 
        """
        try:
            res
        except Exception as e:
            console.print(e, style="bold red")