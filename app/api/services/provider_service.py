from sqlalchemy.orm import Session
from app.models import Provider
from app.api.repositories.provider_repository import ProviderRepository
from app.api.schemas.provider_schema import (
    CreateProviderSchema,
    UpdateProviderSchema,
)


class ProviderService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProviderRepository()

    def get_all_providers(self):
        return self.repository.get_all(self.db)

    def get_provider_by_id(self, provider_id: int):
        return self.repository.get_by_id(self.db, provider_id)

    def get_provider_by_rfc(self, rfc: str):
        return self.repository.get_by_rfc(self.db, rfc.upper())

    def create_provider(self, create_schema: CreateProviderSchema):
        rfc_upper = create_schema.rfc.upper()

        if self.repository.get_by_rfc(self.db, rfc_upper):
            return False, "RFC already registered", None

        new_provider = Provider(
            social_reason=create_schema.social_reason,
            rfc=rfc_upper,
            address=create_schema.address,
        )
        created_provider = self.repository.create(self.db, new_provider)
        return True, "Provider created successfully", created_provider

    def update_provider(self, provider_id: int, update_schema: UpdateProviderSchema):
        existing_provider = self.repository.get_by_id(self.db, provider_id)
        if not existing_provider:
            return False, "Provider not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "rfc" in update_data:
            rfc_upper = update_data["rfc"].upper()
            update_data["rfc"] = rfc_upper

            check_provider = self.repository.get_by_rfc(self.db, rfc_upper)
            if check_provider and check_provider.id != provider_id:
                return False, "RFC already registered", None

        for field, value in update_data.items():
            setattr(existing_provider, field, value)

        updated_provider = self.repository.update(self.db, existing_provider)
        return True, "Provider updated successfully", updated_provider

    def delete_provider(self, provider_id: int):
        existing_provider = self.repository.get_by_id(self.db, provider_id)
        if not existing_provider:
            return False, "Provider not found", None

        deleted_provider = self.repository.delete(self.db, existing_provider)
        return True, "Provider deleted successfully", deleted_provider
