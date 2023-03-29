from deps.fastapi.exception_handlers import http_exception_handler
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from typing import List, Optional
from .. import oauth2

router = APIRouter(prefix="/users", tags=['Users'])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(name=user.name,document=user.document,password=user.password,birth_date=user.birth_date)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_payment_book = models.PaymentBook(payer_id=new_user.id,year=user.payment_book.year)
    db.add(new_payment_book)
    db.commit()
    db.refresh(new_payment_book)
    for i in range(1,13):
        new_month_payment_book = models.MonthlyPayment(payment_book_id=new_payment_book.id,price=0,month=i)
        db.add(new_month_payment_book)
        db.commit()
    return new_user

@router.get("/me",
            response_model=schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user

@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(
        id: int,
        db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user


@router.get("/", response_model=List[schemas.UserOut])
def get_payment_books(db: Session = Depends(get_db)):
    users = db.query(
        models.User
    ).order_by("name").all()
    return users

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)) -> dict:
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(starus_code=404, detail="User Not Found")
    payment_book = db.query(models.PaymentBook).filter(models.PaymentBook.payer_id == user.id).first()
    [ db.delete(m) for m in db.query(models.MonthlyPayment).filter(models.MonthlyPayment.payment_book_id == payment_book.id).all()]
    db.delete(payment_book)
    db.delete(user)
    db.commit()
    return {"ok": True}
