from typing import Optional, List
from pydantic import BaseModel

class PaymentBookOut(BaseModel):
    year: int
    is_payed: bool

class PaymentBookCreate(BaseModel):
    payer: int
    year: int

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    document: str
    is_admin: bool
    payment_books: List[PaymentBookOut] = list()

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    document: str
    password: str


class UserLogin(BaseModel):
    document: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
