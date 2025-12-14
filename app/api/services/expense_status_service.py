from sqlalchemy.orm import Session
from app.models import ExpenseStatus
from app.api.repositories.expense_status_repository import ExpenseStatusRepository
from app.api.schemas.expense_status_schema import (
    CreateExpenseStatusSchema,
    UpdateExpenseStatusSchema,
)


class ExpenseStatusService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ExpenseStatusRepository()

    def get_all_expense_status(self):
        return self.repository.get_all(self.db)

    def get_expense_status_by_id(self, expense_status_id: int):
        return self.repository.get_by_id(self.db, expense_status_id)

    def get_expense_status_by_name(self, expense_status_name: str):
        name_upper = expense_status_name.upper()
        return self.repository.get_by_name(self.db, name_upper)

    def create_expense_status(self, create_schema: CreateExpenseStatusSchema):
        name_upper = create_schema.name.upper()
        if self.repository.get_by_name(self.db, name_upper):
            return False, "Expense status name already registered", None

        new_expense_status = ExpenseStatus(name=name_upper)
        created_expense_status = self.repository.create(self.db, new_expense_status)
        return True, "Expense status created successfully", created_expense_status

    def update_expense_status(
        self, expense_status_id: int, update_schema: UpdateExpenseStatusSchema
    ):
        existing_expense_status = self.repository.get_by_id(self.db, expense_status_id)
        if not existing_expense_status:
            return False, "Expense status not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "name" in update_data:
            name_upper = update_data["name"].upper()
            update_data["name"] = name_upper

        existing_name = self.repository.get_by_name(self.db, name_upper)
        if existing_name and existing_name.id != expense_status_id:
            return False, "Expense status name already registered", None

        for field, value in update_data.items():
            setattr(existing_expense_status, field, value)

        updated_expense_status = self.repository.update(
            self.db, existing_expense_status
        )
        return True, "Expense status updated successfully", updated_expense_status

    def delete_expense_status(self, expense_status_id: int):
        existing_expense_status = self.repository.get_by_id(self.db, expense_status_id)
        if not existing_expense_status:
            return False, "Expense status not found", None

        deleted_expense_status = self.repository.delete(
            self.db, existing_expense_status
        )
        return True, "Expense status deleted successfully", deleted_expense_status
