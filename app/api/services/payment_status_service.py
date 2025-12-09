from sqlalchemy.orm import Session
from app.models import PaymentStatus
from app.api.repositories.payment_status_repository import PaymentStatusRepository
from app.api.schemas.payment_status_schema import (
    CreatePaymentStatusSchema,
    UpdatePaymentStatusSchema,
)


class PaymentStatusService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PaymentStatusRepository()

    def get_all_payment_status(self):
        return self.repository.get_all(self.db)

    def get_payment_status_by_id(self, payment_status_id: int):
        return self.repository.get_by_id(self.db, payment_status_id)

    def get_payment_status_by_name(self, payment_status_name: str):
        name_upper = payment_status_name.upper()
        return self.repository.get_by_name(self.db, name_upper)

    def create_payment_status(self, create_schema: CreatePaymentStatusSchema):
        name_upper = create_schema.name.upper()
        if self.repository.get_by_name(self.db, name_upper):
            return False, "Payment status name already registered", None

        new_payment_status = PaymentStatus(name=name_upper)
        created_payment_status = self.repository.create(self.db, new_payment_status)
        return True, "Payment status created successfully", created_payment_status

    def update_payment_status(
        self, payment_status_id: int, update_schema: UpdatePaymentStatusSchema
    ):
        existing_payment_status = self.repository.get_by_id(self.db, payment_status_id)
        if not existing_payment_status:
            return False, "Payment status not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "name" in update_data:
            name_upper = update_data["name"].upper()
            update_data["name"] = name_upper

        existing_name = self.repository.get_by_name(self.db, name_upper)
        if existing_name and existing_name.id != payment_status_id:
            return False, "Payment status name already registered", None

        for field, value in update_data.items():
            setattr(existing_payment_status, field, value)

        updated_payment_status = self.repository.update(
            self.db, existing_payment_status
        )
        return True, "Payment status updated successfully", updated_payment_status

    def delete_payment_status(self, payment_status_id: int):
        existing_payment_status = self.repository.get_by_id(self.db, payment_status_id)
        if not existing_payment_status:
            return False, "Payment status not found", None

        deleted_payment_status = self.repository.delete(
            self.db, existing_payment_status
        )
        return True, "Payment status deleted successfully", deleted_payment_status
