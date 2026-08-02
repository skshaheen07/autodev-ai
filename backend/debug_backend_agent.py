import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.backend_dev_agent import SYSTEM_PROMPT
from agents.base_agent import call_llm_files

result = call_llm_files(
    SYSTEM_PROMPT,
    "Requirements: ['User authentication', 'Dashboard']\nArchitecture: {'backend': 'FastAPI'}",
    temperature=0.3,
)

print("FILES FOUND:", list(result.get("files", {}).keys()))
print("\n--- RAW RESPONSE ---\n")
print(result.get("raw_response", "(no raw_response key - files were found)"))
