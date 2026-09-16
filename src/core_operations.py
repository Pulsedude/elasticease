from rich.console import Console
from rich.markdown import Markdown
from .config import read, write
from rich.table import Table
from rich.json import JSON
import json
import urllib3

# custom request methods
from .request import get, elastic_base_url

# ai inferences
from .ai_inference import Ollama, LiteLLM

# disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()


class CoreOps:
    def __init__(self):
        configuration = read()
        
        self.ai_mode = configuration if isinstance(configuration, tuple) else configuration.get("elasticease").get("ai_mode")
        self.selected_ai_inference = configuration if isinstance(configuration, tuple) else configuration.get("elasticease").get("selected_ai_inference")
        
        # AI Inferences instances
        self.ollama = Ollama()
        self.litellm = LiteLLM()
    
    def ask_ai(self, prompt: str):
        """Ask AI for data summarization (according to selected AI Inference data summarization request will forward to the selected AI Inference (provider))
        """
        try:
            if isinstance(self.ai_mode, tuple):
                return (False, self.ai_mode[1])
        
            if not isinstance(self.ai_mode, bool):
                return (False, "Please use \"true\" or \"false\" for ai_mode. Change it in configuration")

            
            if isinstance(self.selected_ai_inference, tuple):
                return (False, self.selected_ai_inference[1])
            
            
            if self.selected_ai_inference.lower() == "ollama":
                # ask via ollama
                
                response_via_olama = self.ollama.ask(prompt)
                
                if isinstance(response_via_olama, tuple):
                    return (False, response_via_olama[1])
                
                return response_via_olama
            
            elif self.selected_ai_inference.lower() == "litellm":
                # ask via litellm
                
                response_via_litellm = self.litellm.ask(prompt)
                
                if isinstance(response_via_litellm, tuple):
                    return (False, response_via_litellm[1])

                return response_via_litellm
            
            else:
                return (False, "Unkown AI Inference selected. Please check the configuration")         
                            
        except Exception as e:
            return (False, str(e))
    
    def display_data_with_summary(self, data, prompt: str):
        """Summarize data according to fetched data and print in the console  
        """
        try:
            console.print("Summarizing for you...\n", style="bold green")
            
            ai_summary = self.ask_ai(prompt)
            
            if isinstance(ai_summary, tuple):
                console.print(data)
                console.print(f"Something went wrong while summarizing data! {ai_summary[1]}\n", style="red")
                return
            
            console.print(data)
            print()
            console.print(Markdown(ai_summary))
            print()
            
        except Exception as e:
            return (False, str(e))

    def check_cluster_health(self, ai_summarization: bool = False):
        """Check a cluster health
        """
        try:
            response = get("_cluster/health")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            cluster_health_info_table = Table(
                title=f"Cluster Health | Latency: {response.get("latency")} ms", show_lines=True)

            cluster_health_info_table.add_column(
                "[bright_yellow]Work[/bright_yellow]")
            cluster_health_info_table.add_column(
                "[bright_cyan]Status[/bright_cyan]")

            for work, status in dict(response.get("response")).items():
                cluster_health_info_table.add_row(
                    f"[bold]{work}[/bold]",
                    str(status)
                )

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(cluster_health_info_table)
                return
            
            else:
                self.display_data_with_summary(cluster_health_info_table, f"{response}\nHere is the latest elasticsearch active cluster health data. So please summarize the this given cluster health data into such easier way which is very easy to understand the health of current active cluster. Explain the part of data which is some kind of hard to understand if has.")
            
        except Exception as e:
            console.print(e, style="bold red")
            print()

    def available_shards(self, json_result: bool = False, ai_summarization: bool = False):
        """See available shards
        """
        try:

            response = get("_cat/shards?format=json")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            shards_table = Table(
                title=f"Shards | Latency: {response.get("latency")} ms", show_lines=True)

            if json_result:
                shards_data = {
                    "shards": response.get("response"),
                    "latency": f"{response.get("latency")} ms"
                }
                data_to_display = JSON(json.dumps(shards_data))
            else:
                shards_table.add_column("index")
                shards_table.add_column("shard")
                shards_table.add_column("primary & replica")
                shards_table.add_column("state")
                shards_table.add_column("docs")
                shards_table.add_column("store")
                shards_table.add_column("dataset")
                shards_table.add_column("ip")
                shards_table.add_column("node")

                for shard_info in response.get("response"):
                    shards_table.add_row(
                        f"[bright_cyan]{shard_info.get("index")}[/bright_cyan]",
                        f"[bright_blue]{shard_info.get("shard")}[/bright_blue]",
                        f"[bright_yellow]{shard_info.get("prirep")}[/bright_yellow]",
                        f"[bright_green]{shard_info.get("state")}[/bright_green]",
                        f"[bright_magenta]{shard_info.get("docs")}[/bright_magenta]",
                        f"[turquoise2]{shard_info.get("store")}[/turquoise2]",
                        f"[blue_violet]{shard_info.get("dataset")}[/blue_violet]",
                        f"[light_cyan1]{shard_info.get("ip")}[/light_cyan1]",
                        f"[orange_red1]{shard_info.get("node")}[/orange_red1]",
                    )
                data_to_display = shards_table

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(data_to_display)
                print()
                return
            
            else:
                self.display_data_with_summary(
                    data_to_display,
                    f"{response}\nHere is the latest Elasticsearch shards distribution data across cluster nodes. Please summarize the shard distribution, primary vs replica states, and highlight any unassigned, initializing, or relocating shards in a clear and easy-to-understand way. Explain any potential issues if found."
                )

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def available_indices(self, json_result: bool = False, ai_summarization: bool = False):
        """List all available indices
        """
        try:
            response = get("_cat/indices?format=json")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            indices_table = Table(
                title=f"Indices | Latency: {response.get("latency")} ms", show_lines=True)

            if json_result:
                indices_data = {
                    "indices": response.get("response"),
                    "latency": f"{response.get("latency")} ms"
                }
                data_to_display = JSON(json.dumps(indices_data))
            else:
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

                for index_info in response.get("response"):
                    indices_table.add_row(
                        f"[bright_green]{index_info.get("health")}[/bright_green]" if index_info.get(
                            "health").lower() == "green" else f"[bright_yellow]{index_info.get("health")}[/bright_yellow]",

                        f"[dark_turquoise]{index_info.get("status")}" if index_info.get(
                            "status").lower() == "open" else f"[orange3]{index_info.get("status")}[/orange3]",

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
                data_to_display = indices_table

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(data_to_display)
                print()
                return
            
            else:
                self.display_data_with_summary(
                    data_to_display,
                    f"{response}\nHere is the latest Elasticsearch indices data. Please summarize the indices health status (green, yellow, red), open/close status, document counts, storage sizes, and primary/replica configurations in an easy-to-understand way. Highlight any unhealthy or yellow/red indices, high deleted documents count, or unusual storage sizes if present."
                )

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def ping(self, ai_summarization: bool = False):
        """Ping test on the cluster
        """
        try:
            response = get()

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            ping_info = f"[bold]Base URL:[/bold] [bright_blue]{elastic_base_url}[/bright_blue]\n[bold]Status:[/bold] 🟢 [bright_green]Healthy[/bright_green]\nLatency: {response.get("latency")} ms"

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(
                    f"[bold]Base URL:[/bold] [bright_blue]{elastic_base_url}[/bright_blue]\n[bold]Status:[/bold] 🟢 [bright_green]Healthy[/bright_green]\n")
                console.print(response.get("latency"))
                print()
                return
            
            else:
                self.display_data_with_summary(
                    ping_info,
                    f"{response}\nHere is the ping response from the active Elasticsearch instance. Please give a brief summary of the connection status, cluster name, version, and latency in a clear, concise way."
                )

        except Exception as e:
            console.print(e, style="bold red")
            print()

    def index_details(self, index_name: str, ai_summarization: bool = False):
        """See details of specific target index 
        """
        try:
            response = get(index_name)

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            data_to_display = JSON(json.dumps(response.get("response")))

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(data_to_display)
                print()
                return
            
            else:
                self.display_data_with_summary(
                    data_to_display,
                    f"{response}\nHere are the detailed settings and mappings for index '{index_name}'. Please summarize the index configuration: number of primary and replica shards, key mappings/fields and their data types, aliases, and any special settings in a clear and concise way."
                )
        except Exception as e:
            console.print(e, style="bold red")
            print()

    def master_node(self, json_result: bool = False, ai_summarization: bool = False):
        """See master node
        """
        try:
            response = get("_cat/master?format=json")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            master_node_table = Table(
                title=f"Master Node | Latency: {response.get("latency")} ms", show_lines=True)

            if json_result:
                master_node_data = {
                    "master node": response.get("response"),
                    "latency": f"{response.get("latency")} ms"
                }
                data_to_display = JSON(json.dumps(master_node_data))
            else:
                master_node_table.add_column("id")
                master_node_table.add_column("host")
                master_node_table.add_column("ip")
                master_node_table.add_column("node")

                for master_node_details in response.get("response"):
                    master_node_table.add_row(
                        f"[white]{master_node_details.get("id")}[/white]",
                        f"[bright_cyan]{master_node_details.get("host")}[/bright_cyan]",
                        f"[deep_sky_blue1]{master_node_details.get("ip")}[/deep_sky_blue1]",
                        f"[light_steel_blue1]{master_node_details.get("node")}[/light_steel_blue1]"
                    )
                data_to_display = master_node_table

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(data_to_display)
                print()
                return
            
            else:
                self.display_data_with_summary(
                    data_to_display,
                    f"{response}\nHere is the current active master node data for the Elasticsearch cluster. Please summarize which node is currently elected as master, its IP and host, and briefly explain whether the cluster master is stable and healthy."
                )
        except Exception as e:
            console.print(e, style="bold red")
            print()

    def active_nodes(self, json_result: bool = False, ai_summarization: bool = False):
        """See list of active nodes on cluster
        """
        try:
            response = get("_cat/nodes?format=json")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            nodes_table = Table(
                title=f"Active Nodes | Latency: {response.get("latency")} ms", show_lines=True)

            if json_result:
                active_nodes_data = {
                    "active nodes": response.get("response"),
                    "latency": f"{response.get("latency")} ms"
                }
                data_to_display = JSON(json.dumps(active_nodes_data))
            else:
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

                for node_details in response.get("response"):
                    nodes_table.add_row(
                        f"[white]{node_details.get("ip")}[/white]",
                        f"[bright_blue]{node_details.get("heap.percent")}[/bright_blue]",
                        f"[deep_sky_blue1]{node_details.get("ram.percent")}[/deep_sky_blue1]",
                        f"[deep_sky_blue2]{node_details.get("cpu")}[/deep_sky_blue2]",
                        f"[steel_blue1]{node_details.get("load_1m")}[/steel_blue1]" if node_details.get(
                            "load_1m") else "-",
                        f"[sea_green1]{node_details.get("load_5m")}[/sea_green1]" if node_details.get(
                            "load_5m") else "-",
                        f"[dark_slate_gray2]{node_details.get("load_15m")}[/dark_slate_gray2]" if node_details.get(
                            "load_15m") else "-",
                        f"[light_salmon3]{node_details.get("node.role")}[/light_salmon3]",
                        f"[gold3]{node_details.get("master")}[/gold3]",
                        f"[misty_rose3]{node_details.get("name")}[/misty_rose3]"
                    )
                data_to_display = nodes_table

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(data_to_display)
                print()
                return
            
            else:
                self.display_data_with_summary(
                    data_to_display,
                    f"{response}\nHere is the active nodes resource and performance data for the Elasticsearch cluster. Please summarize the nodes health, identifying any nodes under high JVM heap pressure (above 75%), high RAM, CPU, or elevated load averages (1m, 5m, 15m), and explain the node roles in simple terms."
                )
        except Exception as e:
            console.print(e, style="bold red")
            print()

    def nodes_capacity(self, json_result: bool = False, ai_summarization: bool = False):
        """See the total capacities of storage size and available capacity of active nodes
        """
        try:
            response = get("_cat/allocation?format=json")

            if isinstance(response, tuple):
                console.print(response[1], style="bold red")
                print()
                return

            nodes_capacity_table = Table(
                title=f"Nodes Allocation | Latency: {response.get("latency")} ms", show_lines=True)

            if json_result:
                nodes_alloc_data = {
                    "nodes allocation": response.get("response"),
                    "latency": f"{response.get("latency")} ms"
                }
                data_to_display = JSON(json.dumps(nodes_alloc_data))
            else:
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

                for node_capacity_details in response.get("response"):
                    nodes_capacity_table.add_row(
                        f"[white]{node_capacity_details.get("shards")}[/white]",
                        f"[bright_yellow]{node_capacity_details.get("shards.undesired")}[/bright_yellow]" if node_capacity_details.get(
                            "shards.undesired") else "-",
                        f"[bright_cyan]{node_capacity_details.get("write_load.forecast")}[/bright_cyan]" if node_capacity_details.get(
                            "write_load.forecast") else "-",
                        f"[turquoise2]{node_capacity_details.get("disk.indices.forecast")}[/turquoise2]" if node_capacity_details.get(
                            "disk.indices.forecast") else "-",
                        f"[light_sky_blue1]{node_capacity_details.get("disk.indices")}[/light_sky_blue1]" if node_capacity_details.get(
                            "disk.indices") else "-",
                        f"[orange3]{node_capacity_details.get("disk.used")}[/orange3]" if node_capacity_details.get(
                            "disk.used") else "-",
                        f"[spring_green2]{node_capacity_details.get("disk.avail")}[/spring_green2]" if node_capacity_details.get(
                            "disk.avail") else "-",
                        f"[deep_sky_blue1]{node_capacity_details.get("disk.total")}[/deep_sky_blue1]" if node_capacity_details.get(
                            "disk.total") else "-",
                        f"[bright_magenta]{node_capacity_details.get("disk.percent")}[/bright_magenta]" if node_capacity_details.get(
                            "disk.percent") else "-",
                        f"[bright_cyan]{node_capacity_details.get("host")}[/bright_cyan]" if node_capacity_details.get(
                            "host") else "-",
                        f"[light_cyan1]{node_capacity_details.get("ip")}[/light_cyan1]" if node_capacity_details.get(
                            "ip") else "-",
                        f"[orange_red1]{node_capacity_details.get("node")}[/orange_red1]" if node_capacity_details.get(
                            "node") else "-",
                        f"[light_salmon3]{node_capacity_details.get("node.role")}[/light_salmon3]" if node_capacity_details.get(
                            "node.role") else "-",
                    )
                data_to_display = nodes_capacity_table

            if not (ai_summarization or (isinstance(self.ai_mode, bool) and self.ai_mode)):
                console.print(data_to_display)
                print()
                return
            
            else:
                self.display_data_with_summary(
                    data_to_display,
                    f"{response}\nHere is the Elasticsearch disk capacity and node allocation data. Please summarize the storage allocation across active nodes: total vs used disk percentage, available space, and shard distribution. Point out any node nearing disk watermark thresholds (85% low watermark, 90% high watermark, 95% flood stage) or any storage imbalance."
                )
        except Exception as e:
            console.print(e, style="bold red")
            print()

    # def new_password(self, password: str):
    #     """Change or update a new Elasticsearch password for connection
    #     """
    #     try:
    #         configuration = read()

    #         if isinstance(configuration, tuple):
    #             console.print(configuration[1], style="bold red")
    #             print()
    #             return

    #         configuration.setdefault("elasticease", {})
    #         configuration["elasticease"]["password"] = password
    #         write(configuration)

    #         self.configuration = configuration["elasticease"]
    #         console.print(
    #             f"[bold]New Password:[/bold] [bright_cyan]{password}[/bright_cyan]\n[bright_green]Updated! Now please restart the elasticease to continue.[/bright_green]\n")
    #     except Exception as e:
    #         console.print(e, style="bold red")
    #         print()
