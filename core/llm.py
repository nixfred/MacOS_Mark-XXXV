# core/llm.py
# MARK XXXV macOS — LLM Router
#
# Hybrid model routing:
#   - Text completions → local Ollama (gemma4) when available, Gemini fallback
#   - Live Audio → always Gemini (no local equivalent)
#
# All action files import from here instead of calling Gemini directly.

import json
import os
import sys
from pathlib import Path

try:
    import requests as _requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False


def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


_BASE_DIR        = _get_base_dir()
_API_CONFIG_PATH = _BASE_DIR / "config" / "api_keys.json"

# Ollama config
OLLAMA_URL   = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:26b")

# Cache Ollama availability (checked once)
_ollama_available = None


def _get_api_key() -> str:
    with open(_API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


def _check_ollama() -> bool:
    """Check if Ollama is reachable. Result is cached."""
    global _ollama_available
    if _ollama_available is not None:
        return _ollama_available

    if not _REQUESTS_OK:
        _ollama_available = False
        return False

    try:
        r = _requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            if any(OLLAMA_MODEL in m for m in models):
                _ollama_available = True
                print(f"[LLM] Ollama available — using {OLLAMA_MODEL} for text tasks")
                return True
            else:
                print(f"[LLM] Ollama running but {OLLAMA_MODEL} not found. Available: {models[:5]}")
                _ollama_available = False
                return False
    except Exception:
        pass

    _ollama_available = False
    print(f"[LLM] Ollama not available — using Gemini for all tasks")
    return False


def _ollama_generate(prompt: str, system: str = None) -> str:
    """Call Ollama's generate API."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system

    r = _requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    return r.json().get("response", "").strip()


def _gemini_generate(prompt: str, system: str = None, model_name: str = "gemini-2.5-flash-lite") -> str:
    """Call Gemini's generate API."""
    import google.generativeai as genai
    genai.configure(api_key=_get_api_key())

    kwargs = {}
    if system:
        kwargs["system_instruction"] = system

    model = genai.GenerativeModel(model_name, **kwargs)
    response = model.generate_content(prompt)
    return response.text.strip()


def generate(
    prompt: str,
    system: str = None,
    gemini_model: str = "gemini-2.5-flash-lite",
    prefer_local: bool = True,
) -> str:
    """
    Route text completion to the best available model.

    Args:
        prompt: The prompt to send
        system: Optional system instruction
        gemini_model: Gemini model to use if falling back
        prefer_local: If True, try Ollama first. If False, always use Gemini.

    Returns:
        Generated text response
    """
    if prefer_local and _check_ollama():
        try:
            result = _ollama_generate(prompt, system=system)
            if result:
                return result
            print("[LLM] Ollama returned empty — falling back to Gemini")
        except Exception as e:
            print(f"[LLM] Ollama error: {e} — falling back to Gemini")

    return _gemini_generate(prompt, system=system, model_name=gemini_model)


def get_status() -> dict:
    """Return current routing status for debugging."""
    return {
        "ollama_available": _check_ollama(),
        "ollama_url": OLLAMA_URL,
        "ollama_model": OLLAMA_MODEL,
        "gemini_fallback": True,
    }
