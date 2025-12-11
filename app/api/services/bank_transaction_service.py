from sqlalchemy.orm import Session
from app.models import BankTransaction
from app.api.repositories.bank_transaction_repository import BankTransactionRepository
from app.api.repositories.bank_account_repository import BankAccountRepository
from app.api.repositories.transaction_type_repository import TransactionTypeRepository
from app.api.schemas.bank_transaction_schema import CreateDepositSchema
from app.utils.constants import constants


class BankTransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BankTransactionRepository()
        self.bank_account_repository = BankAccountRepository()
        self.transaction_type_repository = TransactionTypeRepository()

    def get_all_transactions(self):
        return self.repository.get_all(self.db)

    def get_transaction_by_id(self, transaction_id: int):
        return self.repository.get_by_id(self.db, transaction_id)

    def get_transactions_by_account(self, bank_account_id: int):
        return self.repository.get_by_account(self.db, bank_account_id)

    def create_deposit(self, create_schema: CreateDepositSchema):
        bank_account = self.bank_account_repository.get_by_id(
            self.db, create_schema.bank_account_id
        )
        if not bank_account:
            return False, "Bank account not found", None

        income_type = self.transaction_type_repository.get_by_name(
            self.db, constants.TRANSACTION_TYPE_INCOME
        )
        if not income_type:
            return (
                False,
                f"Transaction type {constants.TRANSACTION_TYPE_INCOME} not found",
                None,
            )

        bank_account.balance += create_schema.amount
        self.bank_account_repository.update(self.db, bank_account)

        new_transaction = BankTransaction(
            amount=create_schema.amount,
            description=create_schema.description,
            bank_account_id=bank_account.id,
            transaction_type_id=income_type.id,
            payment_id=None,
        )
        created_transaction = self.repository.create(self.db, new_transaction)

        return True, "Deposit registered successfully", created_transaction
