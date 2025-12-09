from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils import TimestampMixin


class Role(Base, TimestampMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("User", back_populates="role")


class TransactionType(Base, TimestampMixin):
    __tablename__ = "transaction_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    bank_transactions = relationship(
        "BankTransaction", back_populates="transaction_type"
    )


class PaymentStatus(Base, TimestampMixin):
    __tablename__ = "payment_status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    payments = relationship("Payment", back_populates="status")


class ExpenseStatus(Base, TimestampMixin):
    __tablename__ = "expense_status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    expenses = relationship("Expense", back_populates="status")
