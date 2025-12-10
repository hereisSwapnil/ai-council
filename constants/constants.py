# ./constants/constants.py

from enum import Enum

class Model(Enum):
    OLLAMA_GPT_OSS_120B_CLOUD = "gpt-oss:120b-cloud"
    OLLAMA_DEEPSEEK_V3_1_671B_CLOUD = "meta-llama/llama-3.3-70b-instruct:free"
    OLLAMA_QWEN_3_480B_CLOUD = "qwen3-coder:480b-cloud"
    OPEN_ROUTER_GEMMA_3_27B_IT = "google/gemma-3-27b-it:free"
    OPEN_ROUTER_GPT_OSS_20B = "openai/gpt-oss-20b:free"
    OPEN_ROUTER_GROK_4_1_FAST = "x-ai/grok-4.1-fast"
    OPEN_ROUTER_DEEPSEEK_R1T2_CHIMERA = "tngtech/deepseek-r1t2-chimera:free"