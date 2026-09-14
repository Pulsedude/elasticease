from .config import read
import requests
import urllib3
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


configuration = read()
elastic_base_url = None if isinstance(configuration, tuple) else configuration.get(
    "elasticease").get("elasticsearch").get("base_url")

elastic_username = None if isinstance(configuration, tuple) else configuration.get(
    "elasticease").get("elasticsearch").get("username")

elastic_pass = None if isinstance(configuration, tuple) else configuration.get(
    "elasticease").get("elasticsearch").get("password")

verify_certs = None if isinstance(configuration, tuple) else configuration.get(
    "elasticease").get("elasticsearch").get("verify_certs")


def get(endpoint: str = ".") -> dict:
    """Make GET request to elastic API
    """
    try:
        if not elastic_base_url:
            return (False, "Elasticsearch base url not provided!")

        base_url = elastic_base_url + "/" + \
            endpoint if not elastic_base_url.endswith(
                "/") else elastic_base_url + endpoint

        try:
            start = time.perf_counter()

            response = requests.get(
                url=base_url,
                timeout=10,
                auth=(elastic_username, elastic_pass),
                verify=verify_certs
            )

            end = time.perf_counter()
            
        except KeyboardInterrupt:
            return (False, "Request cancelled!")

        if response.status_code != 200:
            return (False, f"Response with code: {response.status_code}!\nPlease check the configuration and username, password")

        return {
            "response": response.json(),
            "latency": f"{((end - start) * 1000):.3f}"
        }

    except Exception as e:
        return (False, str(e))


def post(endpoint: str, data: dict = {}) -> dict:
    """Make POST request to elastic API 
    """
    try:
        if not elastic_base_url:
            return (False, "Elasticsearch base url not provided!")

        base_url = elastic_base_url + "/" + \
            endpoint if not elastic_base_url.endswith(
                "/") else elastic_base_url + endpoint

        data = data

        try:
            start = time.perf_counter()

            response = requests.post(
                url=base_url,
                json=data,
                auth=(elastic_username, elastic_pass),
                timeout=10,
                verify=verify_certs
            )

            end = time.perf_counter()
        
        except KeyboardInterrupt:
            return (False, "Request cancelled!")

        if response.status_code != 200:
            return (False, f"Response with code: {response.status_code}!\nPlease check the configuration and username, password")

        return {
            "response": response.json(),
            "latency": f"{((end - start) * 1000):.3f}"
        }

    except Exception as e:
        return (False, str(e))


def put(endpoint: str, data: dict) -> dict:
    """Make PUT request to elastic API 
    """
    try:
        if not elastic_base_url:
            return (False, "Elasticsearch base url not provided!")

        base_url = elastic_base_url + "/" + \
            endpoint if not elastic_base_url.endswith(
                "/") else elastic_base_url + endpoint

        data = data

        try:
            
            start = time.perf_counter()

            response = requests.put(
                url=base_url,
                json=data,
                auth=(elastic_username, elastic_pass),
                timeout=10,
                verify=verify_certs
            )

            end = time.perf_counter()
        
        except KeyboardInterrupt:
            return (False, "Request cancelled!")

        if response.status_code != 200:
            return (False, f"Response with code: {response.status_code}!\nPlease check the configuration and username, password")
        
        return {
            "response": response.json(),
            "latency": f"{((end - start) * 1000):.3f}"
        }

    except Exception as e:
        return (False, str(e))

def delete(endpoint: str) -> dict:
    """Make DELETE request to elastic API 
    """
    try:
        if not elastic_base_url:
            return (False, "Elasticsearch base url not provided!")

        base_url = elastic_base_url + "/" + \
            endpoint if not elastic_base_url.endswith(
                "/") else elastic_base_url + endpoint

        try:
                
            start = time.perf_counter()

            response = requests.delete(
                url=base_url,
                auth=(elastic_username, elastic_pass),
                timeout=10,
                verify=verify_certs
            )

            end = time.perf_counter()
        
        except KeyboardInterrupt:
            return (False, "Request cancelled!")

        if response.status_code != 200:
            return (False, f"Response with code: {response.status_code}!\nPlease check the configuration and username, password")
        
        return {
            "response": response.json(),
            "latency": f"{((end - start) * 1000):.3f}"
        }

    except Exception as e:
        return (False, str(e))
