from datetime import date
from sqlalchemy.orm import Session
from app.models import Payment, User, BankTransaction
from app.api.repositories.payment_repository import PaymentRepository
from app.api.repositories.expense_repository import ExpenseRepository
from app.api.repositories.expense_status_repository import ExpenseStatusRepository
from app.api.repositories.payment_status_repository import PaymentStatusRepository
from app.api.repositories.bank_account_repository import BankAccountRepository
from app.api.repositories.transaction_type_repository import TransactionTypeRepository
from app.api.schemas.payment_schema import CreatePaymentSchema, ProcessPaymentSchema
from app.utils.constants import constants


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PaymentRepository()
        self.expense_repository = ExpenseRepository()
        self.expense_status_repository = ExpenseStatusRepository()
        self.payment_status_repository = PaymentStatusRepository()
        self.bank_account_repository = BankAccountRepository()
        self.transaction_type_repository = TransactionTypeRepository()

    def get_all_payments(self):
        return self.repository.get_all(self.db)

    def get_payment_by_id(self, payment_id: int):
        return self.repository.get_by_id(self.db, payment_id)

    def create_payment(self, create_schema: CreatePaymentSchema, current_user: User):
        expense = self.expense_repository.get_by_id(self.db, create_schema.expense_id)
        if not expense:
            return False, "Expense not found", None

        if expense.status.name != constants.EXPENSE_STATUS_APPROVED:
            return False, "Expense must be approved to generate a payment order", None

        if self.repository.get_by_expense_id(self.db, expense.id):
            return False, "Payment order already exists for this expense", None

        initial_payment_status = self.payment_status_repository.get_by_name(
            self.db, constants.PAYMENT_STATUS_PENDING
        )
        if not initial_payment_status:
            return (
                False,
                f"Initial status {constants.PAYMENT_STATUS_PENDING.lower()} not found",
                None,
            )

        expense_processed_status = self.expense_status_repository.get_by_name(
            self.db, constants.EXPENSE_STATUS_PROCESSED
        )
        expense.status_id = expense_processed_status.id
        self.expense_repository.update(self.db, expense)

        new_payment = Payment(
            amount=expense.total_amount,
            payment_date=None,
            expense_id=expense.id,
            status_id=initial_payment_status.id,
            created_by_id=current_user.id,
        )

        created_payment = self.repository.create(self.db, new_payment)
        return True, "Payment order generated successfully", created_payment

    def process_payment(
        self, payment_id: int, process_schema: ProcessPaymentSchema, current_user: User
    ):
        payment = self.repository.get_by_id(self.db, payment_id)
        if not payment:
            return False, "Payment not found", None

        if payment.status.name != constants.PAYMENT_STATUS_PENDING:
            return False, "Only pending payments can be processed", None

        if process_schema.action == constants.PAYMENT_ACTION_PAY:
            if not process_schema.bank_account_id:
                return False, "Bank account is required to process payment", None

            bank_account = self.bank_account_repository.get_by_id(
                self.db, process_schema.bank_account_id
            )
            if not bank_account:
                return False, "Bank account not found", None

            if bank_account.balance < payment.amount:
                return False, "Insufficient funds in bank account", None

            paid_status = self.payment_status_repository.get_by_name(
                self.db, constants.PAYMENT_STATUS_PAID
            )

            expense_type = self.transaction_type_repository.get_by_name(
                self.db, constants.TRANSACTION_TYPE_EXPENSES
            )

            bank_account.balance -= payment.amount
            self.bank_account_repository.update(self.db, bank_account)

            payment.status_id = paid_status.id
            payment.payment_date = date.today()
            payment.processed_by_id = current_user.id

            new_transaction = BankTransaction(
                amount=payment.amount,
                description=f"Pago de gasto ID {payment.expense_id}: {payment.expense.description}",
                bank_account_id=bank_account.id,
                transaction_type_id=expense_type.id,
                payment_id=payment.id,
            )
            self.db.add(new_transaction)

            updated_payment = self.repository.update(self.db, payment)
            return True, "Payment executed successfully", updated_payment

        if process_schema.action == constants.PAYMENT_ACTION_CANCEL:
            canceled_status = self.payment_status_repository.get_by_name(
                self.db, constants.PAYMENT_STATUS_CANCELED
            )

            payment.status_id = canceled_status.id
            payment.processed_by_id = current_user.id

            updated_payment = self.repository.update(self.db, payment)
            return True, "Payment canceled successfully", updated_payment

        return False, "Invalid action", None
