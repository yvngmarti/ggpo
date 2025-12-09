from sqlalchemy.orm import Session
from app.models import Role
from app.api.repositories.role_repository import RoleRepository
from app.api.schemas.role_schema import CreateRoleSchema, UpdateRoleSchema


class RoleService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = RoleRepository()

    def get_all_roles(self):
        return self.repository.get_all(self.db)

    def get_role_by_id(self, role_id: int):
        return self.repository.get_by_id(self.db, role_id)

    def get_role_by_name(self, role_name: str):
        name_upper = role_name.upper()
        return self.repository.get_by_name(self.db, name_upper)

    def create_role(self, create_schema: CreateRoleSchema):
        name_upper = create_schema.name.upper()
        if self.repository.get_by_name(self.db, name_upper):
            return False, "Role name already registered", None

        new_role = Role(name=name_upper, description=create_schema.description)
        created_role = self.repository.create(self.db, new_role)
        return True, "Role created successfully", created_role

    def update_role(self, role_id: int, update_schema: UpdateRoleSchema):
        existing_role = self.repository.get_by_id(self.db, role_id)
        if not existing_role:
            return False, "Role not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "name" in update_data:
            name_upper = update_data["name"]
            update_data["name"] = name_upper

            existing_name = self.repository.get_by_name(self.db, name_upper)
            if existing_name and existing_name.id != role_id:
                return False, "Role name already registered", None

        for field, value in update_data.items():
            setattr(existing_role, field, value)

        updated_role = self.repository.update(self.db, existing_role)
        return True, "Role updated successfully", updated_role

    def delete_role(self, role_id: int):
        existing_role = self.repository.get_by_id(self.db, role_id)
        if not existing_role:
            return False, "Role not found", None

        deleted_role = self.repository.delete(self.db, existing_role)
        return True, "Role deleted successfully", deleted_role
