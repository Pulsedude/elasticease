from rich.console import Console
from .config import read, write
from rich.table import Table
from rich.json import JSON
import requests
import json
import urllib3
import sys  

# utils
from .utils import url_validator

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
                return (False, response.json())
            return response
        except Exception as e:
            return (False, e)
        
    def check_cluster_health(self):
        """Check a cluster health
        """
        try:
            cluster_health_info_table = Table(show_lines=True)
            response = self.make_request("_cluster/health")
        
            
            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return 
            
            cluster_health_info_table.add_column("[bright_yellow]Work[/bright_yellow]")
            cluster_health_info_table.add_column("[bright_cyan]Status[/bright_cyan]")

            for work, status in dict(response.json()).items():
                cluster_health_info_table.add_row(
                    f"[bold]{work}[/bold]",
                    str(status)
                )
                
            console.print(cluster_health_info_table)
            print()
            
        except Exception as e:
            console.print(e, style="bold red")
            print()
    
    def available_shards(self, json_result: bool = False):
        """See available shards
        """
        try:
            shards_table = Table(show_lines=True)
            
            response = self.make_request("_cat/shards?format=json")
            
            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            if json_result:
                console.print(JSON(json.dumps(response.json())))
                print()
                return
            
            shards_table.add_column("index")
            shards_table.add_column("shard")
            shards_table.add_column("primary & replica")
            shards_table.add_column("state")
            shards_table.add_column("docs")
            shards_table.add_column("store")
            shards_table.add_column("dataset")
            shards_table.add_column("ip")
            shards_table.add_column("node")
            
            for shard_info in response.json():
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
            print()

    def available_indices(self, json_result: bool = False):
        """List all available indices
        """
        try:
            indices_table = Table(show_lines=True)
            response = self.make_request("_cat/indices?format=json")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            if json_result:
                console.print(JSON(json.dumps(response.json())))
                print()
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
            
            for index_info in response.json():
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
            print()
        
    def ping(self):
        """Ping test on the cluster
        """
        try:
            response = self.make_request()

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            console.print(f"[bold]Base URL:[/bold] [bright_blue]{self.configuration["base_url"]}[/bright_blue]\n[bold]Status:[/bold] 🟢 [bright_green]Healthy[/bright_green]\n")  
            console.print(response.json())     
            print()
             
        except Exception as e:
            console.print(e, style="bold red")
            print()
    
    def index_details(self, index_name: str):
        """See details of specific target index 
        """
        try:
            response = self.make_request(index_name)

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            console.print(JSON(json.dumps(response.json())))
            print() 
        except Exception as e:
            console.print(e, style="bold red")
            print()
        

    def master_nodes(self, json_result: bool = False):
        """See master nodes
        """
        try:
            master_nodes_table = Table(show_lines=True)
            response = self.make_request("_cat/master?format=json")
            
            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            if json_result:
                console.print(JSON(json.dumps(response.json())))
                print()
                return
            
            master_nodes_table.add_column("id")
            master_nodes_table.add_column("host")
            master_nodes_table.add_column("ip")
            master_nodes_table.add_column("node")

            for master_node_details in response.json():
                master_nodes_table.add_row(
                    f"[white]{master_node_details.get("id")}[/white]",
                    f"[bright_cyan]{master_node_details.get("host")}[/bright_cyan]",
                    f"[deep_sky_blue1]{master_node_details.get("ip")}[/deep_sky_blue1]",
                    f"[light_steel_blue1]{master_node_details.get("node")}[/light_steel_blue1]"
                )
            
            console.print(master_nodes_table)
            print()
        except Exception as e:
            console.print(e, style="bold red")
            print()
    
    
            
    def active_nodes(self, json_result: bool = False):
        """See list of active nodes on cluster
        """
        try:
            nodes_table = Table(show_lines=True)
            response = self.make_request("_cat/nodes?format=json")
            
            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            if json_result:
                console.print(JSON(json.dumps(response.json())))
                print()
                return
            
            nodes_table.add_column("ip")
            nodes_table.add_column("heap.percent")
            nodes_table.add_column("ram.percent")
            nodes_table.add_column("cpu")
            nodes_table.add_column("load_1m")
            nodes_table.add_column("load_5m")
            nodes_table.add_column("load_15m")
            nodes_table.add_column("node.role")
            nodes_table.add_column("master")
            nodes_table.add_column("name")
        
            for node_details in response.json():
                nodes_table.add_row(
                    f"[white]{node_details.get("ip")}[/white]",
                    f"[bright_blue]{node_details.get("heap.percent")}[/bright_blue]",
                    f"[deep_sky_blue1]{node_details.get("ram.percent")}[/deep_sky_blue1]",
                    f"[deep_sky_blue2]{node_details.get("cpu")}[/deep_sky_blue2]",
                    f"[steel_blue1]{node_details.get("load_1m")}[/steel_blue1]" if node_details.get("load_1m") else "-",
                    f"[sea_green1]{node_details.get("load_5m")}[/sea_green1]" if node_details.get("load_5m") else "-",
                    f"[dark_slate_gray2]{node_details.get("load_15m")}[/dark_slate_gray2]" if node_details.get("load_15m") else "-",
                    f"[light_salmon3]{node_details.get("node.role")}[/light_salmon3]",
                    f"[gold3]{node_details.get("master")}[/gold3]",
                    f"[misty_rose3]{node_details.get("name")}[/misty_rose3]"
                )
            
            console.print(nodes_table)
            print()
        except Exception as e:
            console.print(e, style="bold red")
            print()
    
    def nodes_capacity(self, json_result: bool = False):
        """See the total capacities of storage size and available capacity of active nodes
        """
        try:
            nodes_capacity_table = Table(show_lines=True)
            response = self.make_request("_cat/allocation?format=json")
            
            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return
            
            if json_result:
                console.print(JSON(json.dumps(response.json())))
                print()
                return

            nodes_capacity_table.add_column("shards")
            nodes_capacity_table.add_column("shards.undesired")
            nodes_capacity_table.add_column("write_load.forecast")
            nodes_capacity_table.add_column("disk.indices.forcast")
            nodes_capacity_table.add_column("disk.indices")
            nodes_capacity_table.add_column("disk.used")
            nodes_capacity_table.add_column("disk.available")
            nodes_capacity_table.add_column("disk.total")
            nodes_capacity_table.add_column("disk.percent")
            nodes_capacity_table.add_column("host")
            nodes_capacity_table.add_column("ip")
            nodes_capacity_table.add_column("node")
            nodes_capacity_table.add_column("node.role")
            
            for node_capacity_details in response.json():
                nodes_capacity_table.add_row(
                    f"[white]{node_capacity_details.get("shards")}[/white]",
                    f"[bright_yellow]{node_capacity_details.get("shards.undesired")}[/bright_yellow]" if node_capacity_details.get("shards.undesired") else "-",
                    f"[bright_cyan]{node_capacity_details.get("write_load.forecast")}[/bright_cyan]" if node_capacity_details.get("write_load.forecast") else "-",
                    f"[turquoise2]{node_capacity_details.get("disk.indices.forecast")}[/turquoise2]" if node_capacity_details.get("disk.indices.forecast") else "-",
                    f"[light_sky_blue1]{node_capacity_details.get("disk.indices")}[/light_sky_blue1]" if node_capacity_details.get("disk.indices") else "-",
                    f"[orange3]{node_capacity_details.get("disk.used")}[/orange3]" if node_capacity_details.get("disk.used") else "-",
                    f"[spring_green2]{node_capacity_details.get("disk.avail")}[/spring_green2]" if node_capacity_details.get("disk.avail") else "-",
                    f"[deep_sky_blue1]{node_capacity_details.get("disk.total")}[/deep_sky_blue1]" if node_capacity_details.get("disk.total") else "-",
                    f"[bright_magenta]{node_capacity_details.get("disk.percent")}[/bright_magenta]" if node_capacity_details.get("disk.percent") else "-",
                    f"[bright_cyan]{node_capacity_details.get("host")}[/bright_cyan]" if node_capacity_details.get("host") else "-",
                    f"[light_cyan1]{node_capacity_details.get("ip")}[/light_cyan1]" if node_capacity_details.get("ip") else "-",
                    f"[orange_red1]{node_capacity_details.get("node")}[/orange_red1]" if node_capacity_details.get("node") else "-",
                    f"[light_salmon3]{node_capacity_details.get("node.role")}[/light_salmon3]" if node_capacity_details.get("node.role") else "-",
                )
            
            console.print(nodes_capacity_table)
            print()
        except Exception as e:
            console.print(e, style="bold red")
            print()
        
    def new_conn_url(self, url: str):
        """Change or update a new Elasticsearch URL for Elasticease
        """
        try:
            check_url = url_validator(url)
            if isinstance(check_url, tuple):
                console.print(check_url[1], style="bold red")
                return
            
            configuration = read()

            if isinstance(configuration, tuple):
                console.print(configuration[1], style="bold red")
                print()
                return

            configuration.setdefault("elasticease", {})
            configuration["elasticease"]["base_url"] = url
            write(configuration)

            self.configuration = configuration["elasticease"]
            console.print(f"[bold]New Base URL:[/bold] [bright_blue]{url}[/bright_blue]\n[bright_green]Updated! Now please restart the elasticease to continue.[/bright_green]\n")
        except Exception as e:
            console.print(e, style="bold red")
            print()
            
    def new_password(self, password: str):
        """Change or update a new Elasticsearch password for connection
        """
        try:
            configuration = read()

            if isinstance(configuration, tuple):
                console.print(configuration[1], style="bold red")
                print()
                return

            configuration.setdefault("elasticease", {})
            configuration["elasticease"]["password"] = password
            write(configuration)

            self.configuration = configuration["elasticease"]
            console.print(f"[bold]New Password:[/bold] [bright_cyan]{password}[/bright_cyan]\n[bright_green]Updated! Now please restart the elasticease to continue.[/bright_green]\n")
        except Exception as e:
            console.print(e, style="bold red")
            print()

    