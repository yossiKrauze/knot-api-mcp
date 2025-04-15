#!/usr/bin/env python3
# ruff: noqa: E402, F401, I001

from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

from data.models import Merchant, MerchantListRequest, ListMerchantsResponse, SessionData, SessionExtensionRequest, SessionExtensionResponse, Session, SwitchCardRequest



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


@app.post("/session/create", response_model=Session)
def create_session(request: SessionData, authorization: str = Depends(verify_auth)):
    # Log the request for debugging
    print(f"Received request: {request}")
    return Session(session_id="test-session-id")


@app.post("/session/extend", response_model=SessionExtensionResponse)
def extend_session(request: SessionExtensionRequest, authorization: str = Depends(verify_auth)):
    # Log the request for debugging
    print(f"Received request: {request}")
    return SessionExtensionResponse(session_id="test-session-id")


@app.post("/card")
def switch_card(request: SwitchCardRequest, authorization: str = Depends(verify_auth)):
    # Log the request for debugging
    print(f"Received request: {request}")
    return {"message": "success"}
