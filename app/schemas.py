from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MonthlyPaymentOut(BaseModel):
    payment_book_id: int
    price: float
    month: int
    is_payed: bool

    class Config:
        orm_mode = True

class MonthlyPaymentCreate(BaseModel):
    payment_book_id: Optional[int] = None
    price: Optional[float] = None
    month: Optional[int] = None
    is_payed: Optional[bool] = False

class PaymentBookOut(BaseModel):
    payer_id: int
    year: int
    is_payed: bool
    monthly_payments: list[MonthlyPaymentOut] = list()

    class Config:
        orm_mode = True

class PaymentBookCreate(BaseModel):
    payer_id: int
    year: int

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    document: str
    is_admin: bool
    payment_books: list[PaymentBookOut] = list()

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    document: str
    password: str
    birth_date: datetime


class UserLogin(BaseModel):
    document: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
