from sqlalchemy.orm import Session
from app.models import User
from app.api.repositories.user_repository import UserRepository
from app.api.repositories.role_repository import RoleRepository
from app.api.schemas.user_schema import CreateUserSchema, UpdateUserSchema
from app.utils.security import SecurityUtils


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()
        self.role_repository = RoleRepository()

    def get_all_users(self):
        return self.repository.get_all(self.db)

    def get_user_by_id(self, user_id: int):
        return self.repository.get_by_id(self.db, user_id)

    def get_user_by_email(self, email: str):
        return self.repository.get_by_email(self.db, email)

    def create_user(self, create_schema: CreateUserSchema):
        email_lower = create_schema.email.lower()
        if self.repository.get_by_email(self.db, email_lower):
            return False, "Email already registered", None

        if not self.role_repository.get_by_id(self.db, create_schema.role_id):
            return False, "Role not found", None

        hashed_password = SecurityUtils.get_password_hash(create_schema.password)

        new_user = User(
            name=create_schema.name,
            last_name=create_schema.last_name,
            email=email_lower,
            password=hashed_password,
            role_id=create_schema.role_id,
        )
        created_user = self.repository.create(self.db, new_user)
        return True, "User created successfully", created_user

    def update_user(self, user_id: int, update_schema: UpdateUserSchema):
        existing_user = self.repository.get_by_id(self.db, user_id)
        if not existing_user:
            return False, "User not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "email" in update_data:
            email_lower = update_data["email"].lower()
            check_user = self.repository.get_by_email(self.db, email_lower)
            if check_user and check_user.id != user_id:
                return False, "Email already registered", None
            update_data["email"] = email_lower

        if "role_id" in update_data:
            if not self.role_repository.get_by_id(self.db, update_data["role_id"]):
                return False, "Role not found", None

        if "password" in update_data:
            hashed_password = SecurityUtils.get_password_hash(update_data["password"])
            update_data["password"] = hashed_password

        for field, value in update_data.items():
            setattr(existing_user, field, value)

        updated_user = self.repository.update(self.db, existing_user)
        return True, "User updated successfully", updated_user
