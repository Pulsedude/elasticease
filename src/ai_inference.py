from litellm import completion
from .config import read
import requests


class Ollama:
    def __init__(self):
        configuration = read().get("elasticease")

        self.base_url = None if isinstance(configuration, tuple) else configuration.get(
            "ai_inference").get("ollama").get("base_url")

        self.model = None if isinstance(configuration, tuple) else configuration.get(
            "ai_inference").get("ollama").get("model")
        
        self.timeout = None if isinstance(configuration, tuple) else configuration.get(
            "ai_inference").get("ollama").get("timeout")

    def ask(self, prompt: str):
        """Ask model running on Ollama engine
        """
        try:
            if not self.base_url or not self.model or not self.timeout:
                return (False, "Please check the ollama configuration!")
                
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            }
            
            req_url = f"{self.base_url}" + "/api/chat" if not self.base_url.endswith("/") else f"{self.base_url}" + "api/chat"
            response = requests.post(req_url, json=data, timeout=self.timeout)
            
            if response.status_code != 200:
                return (False, response.json())
            
            return response.json()["message"]["content"]
        
        except Exception as e:
            return (False, str(e))
        
        
        
class LiteLLM:
    def __init__(self):
        configuration = read().get("elasticease")

        self.model = None if isinstance(configuration, tuple) else configuration.get(
            "ai_inference").get("litellm").get("model")
        
        self.api_key = None if isinstance(configuration, tuple) else configuration.get(
            "ai_inference").get("litellm").get("api_key")

    def ask(self, prompt: str):
        """Ask any such model by the help of Litellm which is basically works as a router to sending query to any such model of any such provider
        """
        try:
            if not self.base_url or not self.model or not self.timeout:
                return (False, "Please check the ollama configuration!")
            
            response = completion(model=self.model, messages=[{"role": "user", "content": prompt}])
    
            return response.choices[0].message.content
        
        except Exception as e:
            return (False, str(e))
