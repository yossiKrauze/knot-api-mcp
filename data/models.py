from pydantic import BaseModel, validator
from typing import Optional, List
from enum import Enum


class Name(BaseModel):
    first_name: str
    last_name: str


class Address(BaseModel):
    street: str
    street2: Optional[str] = None
    city: str
    region: str
    postal_code: str
    country: str


class User(BaseModel):
    name: Name
    phone_number: str
    address: Address


class Card(BaseModel):
    number: str
    expiration: str
    cvv: str
    blocked: Optional[bool] = None
    has_funds: Optional[bool] = None


class CardData(BaseModel):
    task_id: str
    user: User
    card: Card


class Merchant(BaseModel):
    name: str
    external_merchant_id: str
    card_id: str


class MerchantList(BaseModel):
    merchants: List[Merchant]


class JWEData(BaseModel):
    task_id: str
    jwe: str


class SessionData(BaseModel):
    type: str
    external_user_id: str
    card_id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    processor_token: Optional[str] = None
    card: Optional[Card] = None


class MerchantListRequestType(Enum):
    CARD_SWITCHER = "card_switcher"
    TRANSACTION_LINK = "transaction_link"


class MerchantListRequest(BaseModel):
    type: MerchantListRequestType
    platform: Optional[str] = None
    user_agent: Optional[str] = None
    search: Optional[str] = None
    external_user_id: Optional[str] = None
    status: Optional[str] = None


class ListMerchantsResponse(BaseModel):
    merchants: List[Merchant]


class UnlinkMerchant(BaseModel):
    external_user_id: str
    merchant_id: int

    @validator("merchant_id", pre=True)
    def parse_merchant_id(cls, v):
        if isinstance(v, str) and v.isdigit():
            return int(v)
        elif isinstance(v, int):
            return v

        raise ValueError("merchant_id must be an integer")
