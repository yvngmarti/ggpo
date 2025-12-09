from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.services import (
    RoleService,
    TransactionTypeService,
    PaymentStatusService,
    ExpenseStatusService,
    ProjectService,
    BankAccountService,
    ProviderService,
)
from fastapi import Depends


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
