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
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
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
