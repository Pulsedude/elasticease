from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from .config import read
import httpx
import urllib3
import time

console = Console()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Request:
    def __init__(self):
        configuration = read()
        self.elastic_base_url = None if isinstance(configuration, tuple) else configuration.get(
            "elasticease").get("elasticsearch").get("base_url")

        self.elastic_username = None if isinstance(configuration, tuple) else configuration.get(
            "elasticease").get("elasticsearch").get("username")

        self.elastic_pass = None if isinstance(configuration, tuple) else configuration.get(
            "elasticease").get("elasticsearch").get("password")

        self.verify_certs = None if isinstance(configuration, tuple) else configuration.get(
            "elasticease").get("elasticsearch").get("verify_certs")

        self.spinner = Spinner(
            "dots",
            text="Gathering Data...",
            style="bold green"
        )

    async def get(self, endpoint: str = ".") -> dict:
        """Make GET request to elastic API
        """
        try:
            if not self.elastic_base_url:
                return (False, "Elasticsearch base url not provided!")

            req_url = self.elastic_base_url + "/" + \
                endpoint if not self.elastic_base_url.endswith(
                    "/") else self.elastic_base_url + endpoint

            try:
                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.get(
                            url=req_url,
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code != 200:
                return (False, f"Response with code: {response.status_code}!\n{response.json()}")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    async def post(self, endpoint: str, data: dict = {}) -> dict:
        """Make POST request to elastic API 
        """
        try:
            if not self.elastic_base_url:
                return (False, "Elasticsearch base url not provided!")

            req_url = self.elastic_base_url + "/" + \
                endpoint if not self.elastic_base_url.endswith(
                    "/") else self.elastic_base_url + endpoint

            try:
                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.post(
                            url=req_url,
                            json=data,
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code != 200:
                return (False, f"Response with code: {response.status_code}!\n{response.json()}")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    async def put(self, endpoint: str, data: dict = None) -> dict:
        """Make PUT request to elastic API 
        """
        try:
            if not self.elastic_base_url:
                return (False, "Elasticsearch base url not provided!")

            req_url = self.elastic_base_url + "/" + \
                endpoint if not self.elastic_base_url.endswith(
                    "/") else self.elastic_base_url + endpoint

            try:

                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.put(
                            url=req_url,
                            json=data,
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code != 200:
                return (False, f"Response with code: {response.status_code}!\n{response.json()}")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    async def delete(self, endpoint: str) -> dict:
        """Make DELETE request to elastic API 
        """
        try:
            if not self.elastic_base_url:
                return (False, "Elasticsearch base url not provided!")

            req_url = self.elastic_base_url + "/" + \
                endpoint if not self.elastic_base_url.endswith(
                    "/") else self.elastic_base_url + endpoint

            try:

                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.delete(
                            url=req_url,
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code != 200:
                return (False, f"Response with code: {response.status_code}!\n{response.json()}")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))
