from fastapi import APIRouter, Depends
from app.api.services import BankAccountService
from app.api.schemas import bank_account_schema
from app.api.helpers import APIResponse, get_bank_account_service

router = APIRouter(prefix="/bank-accounts", tags=["Bank Accounts"])


@router.get("/", response_model=APIResponse)
def get_bank_accounts(
    service: BankAccountService = Depends(get_bank_account_service),
):
    accounts = service.get_all_bank_accounts()
    data = [
        bank_account_schema.BankAccountResponseSchema.model_validate(acc)
        for acc in accounts
    ]
    message = "Bank accounts retrieved successfully" if data else "No accounts found"
    return APIResponse(status=True, message=message, data=data)


@router.get("/{account_id}", response_model=APIResponse)
def get_bank_account_by_id(
    account_id: int,
    service: BankAccountService = Depends(get_bank_account_service),
):
    account = service.get_bank_account_by_id(account_id)

    if account is None:
        return APIResponse(status=False, message="Bank account not found", data=None)

    data = bank_account_schema.BankAccountResponseSchema.model_validate(account)
    return APIResponse(
        status=True, message="Bank account retrieved successfully", data=data
    )


@router.post("/", response_model=APIResponse)
def create_bank_account(
    create_schema: bank_account_schema.CreateBankAccountSchema,
    service: BankAccountService = Depends(get_bank_account_service),
):
    success, message, account = service.create_bank_account(create_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = bank_account_schema.BankAccountResponseSchema.model_validate(account)
    return APIResponse(status=True, message=message, data=data)


@router.patch("/{account_id}", response_model=APIResponse)
def update_bank_account(
    account_id: int,
    update_schema: bank_account_schema.UpdateBankAccountSchema,
    service: BankAccountService = Depends(get_bank_account_service),
):
    success, message, account = service.update_bank_account(account_id, update_schema)

    if not success:
        return APIResponse(status=False, message=message, data=None)

    data = bank_account_schema.BankAccountResponseSchema.model_validate(account)
    return APIResponse(status=True, message=message, data=data)
