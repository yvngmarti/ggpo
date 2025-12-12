from sqlalchemy.orm import Session
from app.models import Expense, User
from app.api.repositories.expense_repository import ExpenseRepository
from app.api.repositories.project_repository import ProjectRepository
from app.api.repositories.provider_repository import ProviderRepository
from app.api.repositories.expense_status_repository import ExpenseStatusRepository
from app.api.schemas.expense_schema import (
    CreateExpenseSchema,
    UpdateExpenseSchema,
    ReviewExpenseSchema,
)
from app.utils.constants import constants


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ExpenseRepository()
        self.project_repository = ProjectRepository()
        self.provider_repository = ProviderRepository()
        self.expense_status_repository = ExpenseStatusRepository()

    def get_all_expenses(self):
        return self.repository.get_all(self.db)

    def get_expense_by_id(self, expense_id: int):
        return self.repository.get_by_id(self.db, expense_id)

    def create_expense(self, create_schema: CreateExpenseSchema, current_user: User):
        if not self.project_repository.get_by_id(self.db, create_schema.project_id):
            return False, "Project not found", None
        if not self.provider_repository.get_by_id(self.db, create_schema.provider_id):
            return False, "Provider not found", None

        initial_expense_status = self.expense_status_repository.get_by_name(
            self.db, constants.EXPENSE_STATUS_UNDER_REVIEW
        )
        if not initial_expense_status:
            return (
                False,
                f"Initial status {constants.EXPENSE_STATUS_UNDER_REVIEW.lower()} not found",
                None,
            )

        new_expense = Expense(
            description=create_schema.description,
            total_amount=create_schema.total_amount,
            invoice_date=create_schema.invoice_date,
            evidence_url=create_schema.evidence_url,
            project_id=create_schema.project_id,
            provider_id=create_schema.provider_id,
            created_by_id=current_user.id,
            status_id=initial_expense_status.id,
        )
        created_expense = self.repository.create(self.db, new_expense)
        return True, "Expense created successfully", created_expense

    def update_expense(self, expense_id: int, update_schema: UpdateExpenseSchema):
        existing_expense = self.repository.get_by_id(self.db, expense_id)
        if not existing_expense:
            return False, "Expense not found", None

        if existing_expense.status.name == constants.EXPENSE_STATUS_APPROVED:
            return False, "Cannot edit an expense that is already processed", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "project_id" in update_data:
            if not self.project_repository.get_by_id(
                self.db, update_data["project_id"]
            ):
                return False, "Project not found", None
        if "provider_id" in update_data:
            if not self.provider_repository.get_by_id(
                self.db, update_data["provider_id"]
            ):
                return False, "Provider not found", None

        for field, value in update_data.items():
            setattr(existing_expense, field, value)

        reset_status = self.expense_status_repository.get_by_name(
            self.db, constants.EXPENSE_STATUS_UNDER_REVIEW
        )
        existing_expense.status_id = reset_status.id

        updated_expense = self.repository.update(self.db, existing_expense)
        return True, "Expense updated successfully", updated_expense

    def review_expense(
        self, expense_id: int, review_schema: ReviewExpenseSchema, current_user: User
    ):
        existing_expense = self.repository.get_by_id(self.db, expense_id)
        if not existing_expense:
            return False, "Expense not found", None

        if review_schema.action == constants.EXPENSE_ACTION_APPROVE:
            new_status = self.expense_status_repository.get_by_name(
                self.db, constants.EXPENSE_STATUS_APPROVED
            )
            existing_expense.rejection_reason = None
            action_past = constants.EXPENSE_STATUS_APPROVED.lower()

        elif review_schema.action == constants.EXPENSE_ACTION_REJECT:
            if not review_schema.rejection_reason:
                return False, "Rejection reason is required when rejecting", None

            new_status = self.expense_status_repository.get_by_name(
                self.db, constants.EXPENSE_STATUS_REJECTED
            )
            existing_expense.rejection_reason = review_schema.rejection_reason
            action_past = constants.EXPENSE_STATUS_REJECTED.lower()

        else:
            return False, "Invalid action", None

        existing_expense.status_id = new_status.id
        existing_expense.reviewed_by_id = current_user.id

        updated_expense = self.repository.update(self.db, existing_expense)
        return True, f"Expense {action_past} successfully", updated_expense
