from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from .config import read
import httpx
import urllib3
import time
import json
import os

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

    def _build_url(self, endpoint: str = "") -> str:
        """Construct a properly formatted URL by joining the base URL and endpoint."""
        if not self.elastic_base_url:
            return ""
        base = self.elastic_base_url.rstrip("/")
        if not endpoint or endpoint == ".":
            return f"{base}/"
        return f"{base}/{endpoint.lstrip('/')}"

    async def get(self, endpoint: str = ".") -> dict:
        """Make GET request to elastic API
        """
        try:
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            try:
                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.get(
                            url=self._build_url(endpoint),
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code != 200:
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}!\n{err_body}\n")

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
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            try:
                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.post(
                            url=self._build_url(endpoint),
                            json=data,
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code not in (200, 201):
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}!\n{err_body}\n")

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
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            try:

                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.put(
                            url=self._build_url(endpoint),
                            json=data,
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code not in (200, 201):
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}!\n{err_body}\n")

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
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            try:

                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.delete(
                            url=self._build_url(endpoint),
                            timeout=30,
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request cancelled!")

            if response.status_code != 200:
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}!\n{err_body}\n")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    async def bulk_insert(self, index_name: str, data_file: str):
        """Custom request method to insert multiple documents using bulk API 
        """
        try:
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            if not os.path.exists(data_file):
                return (False, f"path: {data_file} does not exist! Please recheck it and try again\n")

            try:
                with open(data_file, "r", encoding="utf-8") as file:
                    docs = json.load(file)

                lines = []

                for doc in docs:
                    action_meta = {}
                    action_meta["index"] = {}
                    action_meta["index"]["_index"] = doc.get(
                        "_index") or doc.get("index") or index_name

                    if "_id" in doc:
                        action_meta["index"]["_id"] = doc.get("_id")

                    elif "id" in doc:
                        action_meta["index"]["_id"] = doc.get("id")

                    lines.append(json.dumps(action_meta))
                    data = {k: v for k, v in doc.items() if k not in (
                        "_index", "index", "_id", "id")}
                    lines.append(json.dumps(data))

                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.post(
                            url=self._build_url(f"{index_name}/_bulk"),
                            content="\n".join(lines) + "\n",
                            timeout=30,
                            headers={
                                "Content-Type": "application/x-ndjson"},
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request Cancelled!")

            if response.status_code != 200:
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}\n{err_body}\n")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    async def bulk_update(self, index_name: str, data_file: str):
        """Custom request method to update multiple existing documents using bulk API 
        """
        try:
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            if not os.path.exists(data_file):
                return (False, f"path: {data_file} does not exist! Please recheck it and try again\n")

            try:
                with open(data_file, "r", encoding="utf-8") as file:
                    docs = json.load(file)

                lines = []
                
                for doc in docs:
                    action_meta = {}
                    action_meta["update"] = {
                        "_id": doc.get("id") or doc.get("_id")
                    }

                    lines.append(json.dumps(action_meta))

                    new_doc = {}
                    new_doc["doc"] = {k: v for k, v in doc.items(
                    ) if k not in ("_index", "index", "_id", "id")}
                    lines.append(json.dumps(new_doc))
                    
                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.post(
                            url=self._build_url(f"{index_name}/_bulk"),
                            content="\n".join(lines) + "\n",
                            timeout=30,
                            headers={
                                "Content-Type": "application/x-ndjson"},
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request Cancelled!")

            if response.status_code != 200:
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}\n{err_body}\n")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    
    async def bulk_delete(self, index_name: str, targets: str):
        """Custom request method to delete multiple existing documents at once using bulk API 
        """
        try:
            if self.elastic_base_url is None or self.elastic_username is None or self.elastic_pass is None or self.verify_certs is None:
                return (False, "Something went wrong! Please recheck the config and try again.\n")

            if not os.path.exists(targets):
                return (False, f"path: {targets} does not exist! Please recheck it and try again\n")

            try:
                with open(targets, "r", encoding="utf-8") as file:
                    docs = json.load(file)

                lines = []
                
                for doc in docs:
                    target = {}
                    index = index_name
                    _id = doc.get("id") or doc.get("_id")
                    
                    target["delete"] = {"_index": index, "_id": _id}
                    lines.append(json.dumps(target))
                
                print("\n".join(lines))
                
                start = time.perf_counter()

                async with httpx.AsyncClient(verify=self.verify_certs) as client:
                    with Live(self.spinner, refresh_per_second=10):

                        response = await client.post(
                            url=self._build_url(f"{index_name}/_bulk"),
                            content="\n".join(lines) + "\n",
                            timeout=30,
                            headers={
                                "Content-Type": "application/x-ndjson"},
                            auth=(self.elastic_username, self.elastic_pass)
                        )

                end = time.perf_counter()

            except KeyboardInterrupt:
                return (False, "Request Cancelled!")

            if response.status_code != 200:
                try:
                    err_body = response.json()
                except Exception:
                    err_body = response.text
                return (False, f"Response with code: {response.status_code}\n{err_body}\n")

            return {
                "response": response.json(),
                "latency": f"{((end - start) * 1000):.3f}"
            }

        except Exception as e:
            return (False, str(e))

    
    