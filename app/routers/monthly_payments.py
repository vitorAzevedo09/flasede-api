
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .. import oauth2
from typing import List

router = APIRouter(prefix="/monthly_payments", tags=['MonthlyPayments'])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MonthlyPaymentOut,
)
def create_monthly_payments(monthly_payment: schemas.MonthlyPaymentCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Permission Denied")
    new_monthly_payment = models.MonthlyPayment(**monthly_payment.dict())
    db.add(new_monthly_payment)
    db.commit()
    db.refresh(new_monthly_payment)
    return new_monthly_payment

@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MonthlyPaymentOut,
)
def update_monthly_payments(id: int,
                            monthly_payment: schemas.MonthlyPaymentCreate,
                            db: Session = Depends(get_db),
                            current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Permission Denied")
    old_monthly_payment = db.query(models.MonthlyPayment).filter(models.MonthlyPayment.id == id).first()
    if not old_monthly_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'old_account with the id {monthly_payment.id} is not available')
    mp = monthly_payment.dict(exclude_unset=True)
    for key, value in mp.items():
        setattr(old_monthly_payment,key,value)
    db.add(old_monthly_payment)
    db.commit()
    return old_monthly_payment

@router.get('/{id}', response_model=schemas.MonthlyPaymentOut)
def get_monthly_payment(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):
    monthly_payment = db.query(models.MonthlyPayment).filter(models.MonthlyPayment.id == id).first()
    if not monthly_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"PaymentBook with id: {id} does not exist")
    return monthly_payment

@router.get("/", response_model=List[schemas.MonthlyPaymentOut])
def get_monthly_payments(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    monthly_payments = db.query(
        models.MonthlyPayment
    ).order_by("month").all()
    return monthly_payments
