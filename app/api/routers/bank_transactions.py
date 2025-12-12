from fastapi import APIRouter, Depends
from app.api.services.bank_transaction_service import BankTransactionService
from app.api.schemas import bank_transaction_schema
from app.api.helpers import (
    APIResponse,
    get_bank_transaction_service,
    RoleChecker,
)
from app.utils.constants import constants
from app.models import User

router = APIRouter(prefix="/bank-transactions", tags=["Bank Transactions"])


@router.get("", response_model=APIResponse)
def get_transactions(
    service: BankTransactionService = Depends(get_bank_transaction_service),
    current_user: User = Depends(
        RoleChecker([constants.ROLE_DIRECTOR, constants.ROLE_TREASURER])
    ),
):
    transactions = service.get_all_transactions()
    data = [
        bank_transaction_schema.BankTransactionResponseSchema.model_validate(t)
        for t in transactions
    ]
    message = "Transactions retrieved successfully" if data else "No transactions found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/account/{account_id}", response_model=APIResponse)
def get_transactions_by_account(
    account_id: int,
    service: BankTransactionService = Depends(get_bank_transaction_service),
    current_user: User = Depends(
        RoleChecker([constants.ROLE_DIRECTOR, constants.ROLE_TREASURER])
    ),
):
    transactions = service.get_transactions_by_account(account_id)
    data = [
        bank_transaction_schema.BankTransactionResponseSchema.model_validate(t)
        for t in transactions
    ]
    message = "Transactions retrieved successfully" if data else "No transactions found"
    return APIResponse(status=True, message=message, data=data)


@router.post("/deposit", response_model=APIResponse)
def create_deposit(
    create_schema: bank_transaction_schema.CreateDepositSchema,
    service: BankTransactionService = Depends(get_bank_transaction_service),
    current_user: User = Depends(RoleChecker([constants.ROLE_TREASURER])),
):
    success, message, transaction = service.create_deposit(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = bank_transaction_schema.BankTransactionResponseSchema.model_validate(
        transaction
    )
    return APIResponse(status=True, message=message, data=data)
