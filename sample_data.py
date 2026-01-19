#sample_data.py
# Updated for Reliability & India Region Availability
MODELS = {
    "Amazon Nova Pro": {
        "id": "us.amazon.nova-pro-v1:0", # Use IDs for API calls
        "type": "Teacher",
        "latency_ms": 180, 
        "throughput_rps": 50,
        "fallback_prices": (0.0008, 0.0032) # In case API fails
    },
    "Anthropic Claude 3.5 Sonnet": {
        "id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "type": "Teacher",
        "latency_ms": 210,
        "throughput_rps": 45,
        "fallback_prices": (0.0030, 0.0150)
    },
    "Meta Llama 3.1 70B": {
        "id": "meta.llama3-1-70b-instruct-v1:0",
        "type": "Teacher",
        "latency_ms": 240,
        "throughput_rps": 35,
        "fallback_prices": (0.00099, 0.00125)
    },
    "Amazon Nova Lite": {
        "id": "us.amazon.nova-lite-v1:0",
        "type": "Student",
        "latency_ms": 90,
        "throughput_rps": 90,
        "fallback_prices": (0.00006, 0.00024)
    },
    "Anthropic Claude 3 Haiku": {
        "id": "anthropic.claude-3-haiku-20240307-v1:0",
        "type": "Student",
        "latency_ms": 100,
        "throughput_rps": 85,
        "fallback_prices": (0.00025, 0.00125)
    }
}

MODEL_COMPATIBILITY = {
    "Amazon Nova Pro": ["Amazon Nova Lite"],
    "Anthropic Claude 3.5 Sonnet": ["Anthropic Claude 3 Haiku"],
    "Meta Llama 3.1 70B": ["Meta Llama 3.1 8B"]
}

PREDEFINED_USE_CASES = {
    "2-Page PDF Summarization": (4000, 400),
    "Code Generation": (2000, 1000),
    "QA on Docs": (3000, 200),
}

TEACHER_MODELS = [k for k, v in MODELS.items() if v["type"] == "Teacher"]