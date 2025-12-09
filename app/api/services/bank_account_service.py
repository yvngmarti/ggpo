from sqlalchemy.orm import Session
from app.models import BankAccount
from app.api.repositories.bank_account_repository import BankAccountRepository
from app.api.schemas.bank_account_schema import (
    CreateBankAccountSchema,
    UpdateBankAccountSchema,
)


class BankAccountService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BankAccountRepository()

    def get_all_bank_accounts(self):
        return self.repository.get_all(self.db)

    def get_bank_account_by_id(self, account_id: int):
        return self.repository.get_by_id(self.db, account_id)

    def get_bank_account_by_number(self, account_number: str):
        return self.repository.get_by_account_number(self.db, account_number)

    def create_bank_account(self, create_schema: CreateBankAccountSchema):
        if self.repository.get_by_account_number(self.db, create_schema.account_number):
            return False, "Account number already registered", None

        new_account = BankAccount(
            name=create_schema.name,
            account_number=create_schema.account_number,
            balance=create_schema.balance,
        )
        created_account = self.repository.create(self.db, new_account)
        return True, "Bank account created successfully", created_account

    def update_bank_account(
        self, account_id: int, update_schema: UpdateBankAccountSchema
    ):
        existing_account = self.repository.get_by_id(self.db, account_id)
        if not existing_account:
            return False, "Bank account not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "account_number" in update_data:
            new_number = update_data["account_number"]
            duplicate_check = self.repository.get_by_account_number(self.db, new_number)

            if duplicate_check and duplicate_check.id != account_id:
                return (
                    False,
                    "Account number already registered by another account",
                    None,
                )

        for field, value in update_data.items():
            setattr(existing_account, field, value)

        updated_account = self.repository.update(self.db, existing_account)
        return True, "Bank account updated successfully", updated_account
