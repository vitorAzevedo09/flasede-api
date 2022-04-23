
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import oauth2
from typing import List, Optional

router = APIRouter(prefix="/payment_books", tags=['Users'])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PaymentBookOut,
)
def create_payment_book(payment_book: schemas.PaymentBookCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Permission Denied")
    new_payment_book = models.PaymentBook(**payment_book.dict())
    db.add(new_payment_book)
    db.commit()
    db.refresh(new_payment_book)
    return new_payment_book


@router.get('/{id}', response_model=schemas.PaymentBookOut)
def get_payment_book(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):
    payment_book = db.query(models.PaymentBook).filter(models.PaymentBook.id == id).first()
    if not payment_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"PaymentBook with id: {id} does not exist")
    return payment_book

@router.get("/", response_model=List[schemas.UserOut])
def get_payment_books(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              search: Optional[int] = 1):
    payment_book = db.query(
        models.PaymentBook
    ).filter(
        models.PaymentBook.year.contains(search)
    ).all()
    return payment_book
