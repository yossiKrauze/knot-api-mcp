from data.models import Merchant, MerchantListRequest, ListMerchantsResponse
from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
import sys
import os

# Add the parent directory to sys.path to allow importing from data.models
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

app = FastAPI()


def verify_auth(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Basic "):
        raise HTTPException(
            status_code=401, detail="Invalid or missing Authorization header")
    return authorization


@app.post("/merchant/list", response_model=ListMerchantsResponse)
def list_merchants(request: MerchantListRequest, authorization: str = Depends(verify_auth)):
    # Log the request for debugging
    print(f"Received request: {request}")

    # Filter logic could be implemented here based on request parameters
    # For now, return a static list of merchants
    return ListMerchantsResponse(merchants=[
        Merchant(name="Starbucks", external_merchant_id="starbucks",
                 card_id="card_123"),
        Merchant(name="Costa Coffee",
                 external_merchant_id="costa", card_id="card_456"),
        Merchant(name="Amazon", external_merchant_id="amazon",
                 card_id="card_789"),
        Merchant(name="Walmart", external_merchant_id="walmart",
                 card_id="card_101"),
        Merchant(name="Target", external_merchant_id="target",
                 card_id="card_102")
    ])
