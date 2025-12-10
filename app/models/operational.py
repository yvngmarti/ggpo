from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False
    )

    role = relationship("Role", back_populates="users")

    created_expenses = relationship(
        "Expense", back_populates="created_by", foreign_keys="Expense.created_by_id"
    )
    reviewed_expenses = relationship(
        "Expense", back_populates="reviewed_by", foreign_keys="Expense.reviewed_by_id"
    )

    created_payments = relationship(
        "Payment", back_populates="created_by", foreign_keys="Payment.created_by_id"
    )

    processed_payments = relationship(
        "Payment", back_populates="processed_by", foreign_keys="Payment.processed_by_id"
    )


class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    code = Column(String, unique=True)
    budget = Column(Float)

    expenses = relationship("Expense", back_populates="project")


class Provider(Base, TimestampMixin):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    social_reason = Column(String)
    rfc = Column(String, unique=True)
    address = Column(String)

    expenses = relationship("Expense", back_populates="provider")


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    account_number = Column(String, unique=True)
    balance = Column(Float, default=0.0)

    bank_transactions = relationship(
        "BankTransaction",
        back_populates="bank_account",
    )


class Expense(Base, TimestampMixin):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    total_amount = Column(Float, nullable=False)
    invoice_date = Column(Date, nullable=False)
    evidence_url = Column(String)
    rejection_reason = Column(Text)

    created_by_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    reviewed_by_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"))
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False
    )
    provider_id = Column(
        Integer, ForeignKey("providers.id", ondelete="RESTRICT"), nullable=False
    )
    status_id = Column(
        Integer, ForeignKey("expense_status.id", ondelete="RESTRICT"), nullable=False
    )

    created_by = relationship(
        "User", back_populates="created_expenses", foreign_keys=[created_by_id]
    )
    reviewed_by = relationship(
        "User", back_populates="reviewed_expenses", foreign_keys=[reviewed_by_id]
    )
    project = relationship("Project", back_populates="expenses")
    provider = relationship("Provider", back_populates="expenses")
    status = relationship("ExpenseStatus", back_populates="expenses")

    payment = relationship("Payment", back_populates="expense", uselist=False)


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_date = Column(Date)

    expense_id = Column(
        Integer,
        ForeignKey("expenses.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    status_id = Column(
        Integer, ForeignKey("payment_status.id", ondelete="RESTRICT"), nullable=False
    )
    created_by_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    processed_by_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"))

    expense = relationship("Expense", back_populates="payment", uselist=False)
    status = relationship("PaymentStatus", back_populates="payments")
    created_by = relationship(
        "User", back_populates="created_payments", foreign_keys=[created_by_id]
    )
    processed_by = relationship(
        "User", back_populates="processed_payments", foreign_keys=[processed_by_id]
    )

    bank_transaction = relationship(
        "BankTransaction", back_populates="payment", uselist=False
    )


class BankTransaction(Base, TimestampMixin):
    __tablename__ = "bank_transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)

    bank_account_id = Column(
        Integer, ForeignKey("bank_accounts.id", ondelete="RESTRICT"), nullable=False
    )
    transaction_type_id = Column(
        Integer, ForeignKey("transaction_types.id", ondelete="RESTRICT"), nullable=False
    )
    payment_id = Column(
        Integer,
        ForeignKey("payments.id", ondelete="RESTRICT"),
        unique=True,
    )

    bank_account = relationship("BankAccount", back_populates="bank_transactions")
    transaction_type = relationship(
        "TransactionType", back_populates="bank_transactions"
    )
    payment = relationship("Payment", back_populates="bank_transaction", uselist=False)
