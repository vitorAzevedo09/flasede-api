from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    ''' Usuario '''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    document = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    cdreated_at = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         server_default=text('now()'))


class PaymentBook(Base):
    ''' Carnê '''
    __tablename__ = "payment_books"
    id = Column(Integer, primary_key=True, nullable=False)
    year = Column(Integer, nullable=False)
    is_payed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    payer_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)
    payer = relationship("User")


class MonthlyPayment(Base):
    ''' Mensalidade '''
    __tablename__ = "monthly_payments"
    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(Numeric, primary_key=True, nullable=False)
    payment_book_id = Column(Integer,
                             ForeignKey("payment_books.id",
                                        ondelete="CASCADE"),
                             nullable=False)
    payment_book = relationship("PaymentBook")
