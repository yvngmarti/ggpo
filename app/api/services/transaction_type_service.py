from sqlalchemy.orm import Session
from app.models import TransactionType
from app.api.repositories.transaction_type_repository import TransactionTypeRepository
from app.api.schemas.transaction_type_schema import (
    CreateTransactionTypeSchema,
    UpdateTransactionTypeSchema,
)


class TransactionTypeService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TransactionTypeRepository()

    def get_all_transaction_types(self):
        return self.repository.get_all(self.db)

    def get_transaction_type_by_id(self, transaction_type_id: int):
        return self.repository.get_by_id(self.db, transaction_type_id)

    def get_transaction_type_by_name(self, transaction_type_name: str):
        name_upper = transaction_type_name.upper()
        return self.repository.get_by_name(self.db, name_upper)

    def create_transaction_type(self, create_schema: CreateTransactionTypeSchema):
        name_upper = create_schema.name.upper()
        if self.repository.get_by_name(self.db, name_upper):
            return False, "Transaction type name already registered", None

        new_transaction_type = TransactionType(name=name_upper)
        created_transaction_type = self.repository.create(self.db, new_transaction_type)
        return True, "Transaction type created successfully", created_transaction_type

    def update_transaction_type(
        self, transaction_type_id: int, update_schema: UpdateTransactionTypeSchema
    ):
        existing_transaction_type = self.repository.get_by_id(
            self.db, transaction_type_id
        )
        if not existing_transaction_type:
            return False, "Transaction type not found", None

        if update_schema.name:
            name_upper = update_schema.name.upper()
            existing_name = self.repository.get_by_name(self.db, name_upper)
            if existing_name and existing_name.id != transaction_type_id:
                return False, "Transaction type name already registered", None

        update_data = update_schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_transaction_type, field, value)

        updated_transaction_type = self.repository.update(
            self.db, existing_transaction_type
        )
        return True, "Transaction type updated successfully", updated_transaction_type

    def delete_transaction_type(self, transaction_type_id: int):
        existing_transaction_type = self.repository.get_by_id(
            self.db, transaction_type_id
        )
        if not existing_transaction_type:
            return False, "Transaction type not found", None

        deleted_transaction_type = self.repository.delete(
            self.db, existing_transaction_type
        )
        return True, "Transaction type deleted successfully", deleted_transaction_type
