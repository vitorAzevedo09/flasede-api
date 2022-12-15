from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class User(Base):
    ''' Usuario '''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    document = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String, nullable=False)
    birth_date = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    logged_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    payment_books = relationship("PaymentBook", back_populates="payer")


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
    payer = relationship("User", back_populates="payment_books")
    monthly_payments = relationship("MonthlyPayment", back_populates="payment_book")


class MonthlyPayment(Base):
    ''' Mensalidade '''
    __tablename__ = "monthly_payments"
    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(Numeric, nullable=False)
    month = Column(Integer,nullable=False)
    is_payed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    payment_book_id = Column(Integer,
                             ForeignKey("payment_books.id",
                                        ondelete="CASCADE"),
                             nullable=False)
    payment_book = relationship("PaymentBook", back_populates="monthly_payments")
