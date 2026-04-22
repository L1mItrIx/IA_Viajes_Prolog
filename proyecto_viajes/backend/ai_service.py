import json
import os
import urllib.error
import urllib.request

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")


def generar_texto(prompt: str) -> str | None:
    try:
        payload = json.dumps(
            {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 140,
                },
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        texto = data.get("response", "").strip()
        return texto or None
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as e:
        print(f"Ollama no disponible, usando fallback local: {e}")
        return None
