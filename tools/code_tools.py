from core.llm import OllamaLLM
from core.prompts import CODING_SYSTEM_PROMPT


llm = OllamaLLM()


def analyze_code(user_request: str) -> str:
    prompt = f"""
User coding request:

{user_request}

Return:
1. Problem found
2. Fixed code
3. What changed
"""
    return llm.generate(prompt=prompt, system=CODING_SYSTEM_PROMPT)
