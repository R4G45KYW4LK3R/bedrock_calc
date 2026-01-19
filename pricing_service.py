import boto3
import json
import streamlit as st

class BedrockPricing:
    def __init__(self, region="ap-south-1"):
        # The Pricing API only exists in us-east-1, but can query prices for any region
        self.client = boto3.client('pricing', region_name='us-east-1')
        self.region = region
        self.region_map = {"ap-south-1": "Asia Pacific (Mumbai)"}

    @st.cache_data(ttl=86400) # Cache for 24 hours
    def get_model_price(_self, model_name: str):
        """Fetch live prices from AWS Price List API"""
        try:
            # Note: Model names in Price List API often vary slightly from Bedrock IDs
            # We filter by service and region
            response = _self.client.get_products(
                ServiceCode='AmazonBedrock',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'regionCode', 'Value': _self.region},
                    {'Type': 'TERM_MATCH', 'Field': 'modelName', 'Value': model_name}
                ]
            )
            
            prices = {"input": 0.0, "output": 0.0, "provisioned": 0.0}
            
            for item in response['PriceList']:
                product = json.loads(item)
                terms = product['terms']['OnDemand']
                for term_val in terms.values():
                    for price_dim in term_val['priceDimensions'].values():
                        desc = price_dim['description'].lower()
                        price_per_unit = float(price_dim['pricePerUnit']['USD'])
                        
                        if "input" in desc:
                            prices["input"] = price_per_unit
                        elif "output" in desc:
                            prices["output"] = price_per_unit
            
            return prices
        except Exception:
            return None # Fallback logic in main app