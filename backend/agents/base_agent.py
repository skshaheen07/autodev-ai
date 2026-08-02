import re
import json
import time
from groq import RateLimitError
from langchain_groq import ChatGroq

from app.core.config import settings

FENCE = chr(96) * 3


def get_llm(temperature: float = 0.3):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=settings.GROQ_API_KEY,
    )


def _invoke_with_backoff(llm, prompt: str, max_retries: int = 4):
    delay = 3
    for attempt in range(max_retries):
        try:
            return llm.invoke(prompt)
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("Unreachable")


def _extract_json(text: str) -> str:
    text = text.strip()
    if text.startswith(FENCE):
        text = re.sub(r"^" + FENCE + r"(json)?", "", text).strip()
        text = re.sub(FENCE + r"$", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def call_llm_json(system_prompt: str, user_content: str, temperature: float = 0.3) -> dict:
    llm = get_llm(temperature=temperature)
    full_prompt = system_prompt + "\n\n" + user_content
    response = _invoke_with_backoff(llm, full_prompt)
    raw = response.content

    try:
        return json.loads(_extract_json(raw))
    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM response as JSON", "raw_response": raw}


def call_llm_files(system_prompt: str, user_content: str, temperature: float = 0.3) -> dict:
    llm = get_llm(temperature=temperature)
    instructions = (
        "IMPORTANT OUTPUT FORMAT: For each file, output a line exactly like:\n"
        "### FILE: <relative/path/to/file>\n"
        "followed by a code block (three backtick characters) containing the full file content.\n"
        "Do not add any explanation before, between, or after the files.\n\n"
    )
    full_prompt = system_prompt + "\n\n" + instructions + user_content
    response = _invoke_with_backoff(llm, full_prompt)
    raw = response.content

    files = {}
    pattern = r"###\s*FILE:\s*(.+?)\s*\n" + FENCE + r"[a-zA-Z]*\n(.*?)" + FENCE
    matches = re.findall(pattern, raw, re.DOTALL)
    for path, content in matches:
        files[path.strip()] = content.strip()

    if not files:
        return {"files": {}, "raw_response": raw}
    return {"files": files}
