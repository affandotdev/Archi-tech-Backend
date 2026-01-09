import requests

import os

# Use host.docker.internal for Docker/Windows, or localhost for local dev
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
# Default to llama3, but allow fallback or configuration if needed
MODEL_NAME = "llama3" 

def generate_response(prompt: str, system: str = None) -> str:
    """
    Generates a response using the local Ollama instance.
    Sends a request to http://localhost:11434/api/generate.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    if system:
        payload["system"] = system
    
    try:
        # 60s timeout might be tight for local LLMs on older hardware, 
        # but prevents indefinite hanging.
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=90)
        response.raise_for_status()
        
        data = response.json()
        return data.get("response", "")
        
    except requests.exceptions.ConnectionError:
        raise Exception("Ollama is not running. Please run 'ollama run llama3' in your terminal.")
    except Exception as e:
        raise Exception(f"Ollama Error: {str(e)}")
