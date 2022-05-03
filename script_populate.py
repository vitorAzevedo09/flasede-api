import csv
from app import models
from datetime import datetime
from app.database import SessionLocal
from app.utils import hash
from app import models

# with open("socios_flasede.csv") as file:
    # data = csv.DictReader(file)
    # db = SessionLocal()
    # for r in data:
        # password = r['Data de Nascimento'].split("/")
        # hashed_password =  hash(password[1]+password[0]+password[2])
        # user = models.User(
            # first_name=r["Nome"],
            # last_name=r["Sobrenome"],
            # password=hashed_password,
            # document=r["CPF"],
            # birth_date=datetime.strptime(
                # r['Data de Nascimento'],
                # "%m/%d/%Y"
            # )
        # )
        # db.add(user)
        # db.commit()

# db = SessionLocal()
# for u in db.query(models.User).filter( 2 != models.User.id != 1).all():
    # pb = models.PaymentBook(payer_id=u.id,year=2022)
    # db.add(pb)
    # db.commit()

db = SessionLocal()
for p in db.query( models.PaymentBook ).all():
    for i in range(1,13):
        new_month_payment_book = models.MonthlyPayment(payment_book_id=p.id,price=0,month=i)
        db.add(new_month_payment_book)
        db.commit()
        db.refresh(new_month_payment_book)
