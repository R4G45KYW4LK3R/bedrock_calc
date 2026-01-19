# roi_function.py
def calculate_tco(model_meta, prices, input_tokens, output_tokens, monthly_requests, is_custom=False):
    # Prices are per 1000 tokens from API
    p_in = prices['input']
    p_out = prices['output']
    
    inference_cost = ((input_tokens * p_in) + (output_tokens * p_out)) / 1000 * monthly_requests
    
    # India Region specifics
    storage_cost = 1.95 if is_custom else 0
    data_transfer_gb = (output_tokens * monthly_requests * 4) / (1024**3)
    data_transfer_cost = data_transfer_gb * 0.09 
    
    total_tco = inference_cost + storage_cost + data_transfer_cost
    
    return {
        "total_tco": total_tco,
        "inference_cost": inference_cost,
        "latency_ms": model_meta["latency_ms"]
    }