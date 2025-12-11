from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.api.services import (
    AuthService,
    RoleService,
    TransactionTypeService,
    PaymentStatusService,
    ExpenseStatusService,
    ProjectService,
    BankAccountService,
    ProviderService,
    UserService,
    ExpenseService,
    PaymentService,
    BankTransactionService,
)


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


def get_role_service(db: Session = Depends(get_db)):
    return RoleService(db)


def get_transaction_type_service(db: Session = Depends(get_db)):
    return TransactionTypeService(db)


def get_payment_status_service(db: Session = Depends(get_db)):
    return PaymentStatusService(db)


def get_expense_status_service(db: Session = Depends(get_db)):
    return ExpenseStatusService(db)


def get_project_service(db: Session = Depends(get_db)):
    return ProjectService(db)


def get_bank_account_service(db: Session = Depends(get_db)):
    return BankAccountService(db)


def get_provider_service(db: Session = Depends(get_db)):
    return ProviderService(db)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


def get_expense_service(db: Session = Depends(get_db)):
    return ExpenseService(db)


def get_payment_service(db: Session = Depends(get_db)):
    return PaymentService(db)


def get_bank_transaction_service(db: Session = Depends(get_db)):
    return BankTransactionService(db)
