from sqlalchemy.orm import Session
from app.models import Project
from app.api.repositories.project_repository import ProjectRepository
from app.api.schemas.project_schema import (
    CreateProjectSchema,
    UpdateProjectSchema,
)


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProjectRepository()

    def get_all_projects(self):
        return self.repository.get_all(self.db)

    def get_project_by_id(self, project_id: int):
        return self.repository.get_by_id(self.db, project_id)

    def get_project_by_code(self, project_code: str):
        code_upper = project_code.upper()
        return self.repository.get_by_code(self.db, code_upper)

    def create_project(self, create_schema: CreateProjectSchema):
        code_upper = create_schema.code.upper()

        if self.repository.get_by_code(self.db, code_upper):
            return False, "Project code already registered", None

        new_project = Project(
            name=create_schema.name,
            description=create_schema.description,
            code=code_upper,
            budget=create_schema.budget,
        )
        created_project = self.repository.create(self.db, new_project)
        return True, "Project created successfully", created_project

    def update_project(self, project_id: int, update_schema: UpdateProjectSchema):
        existing_project = self.repository.get_by_id(self.db, project_id)
        if not existing_project:
            return False, "Project not found", None

        update_data = update_schema.model_dump(exclude_unset=True)

        if "code" in update_data:
            code_upper = update_data["code"].upper()
            update_data["code"] = code_upper

            existing_code = self.repository.get_by_code(self.db, code_upper)
            if existing_code and existing_code.id != project_id:
                return False, "Project code already registered", None

        for field, value in update_data.items():
            setattr(existing_project, field, value)

        updated_project = self.repository.update(self.db, existing_project)
        return True, "Project updated successfully", updated_project

    def delete_project(self, project_id: int):
        existing_project = self.repository.get_by_id(self.db, project_id)
        if not existing_project:
            return False, "Project not found", None

        deleted_project = self.repository.delete(self.db, existing_project)
        return True, "Project deleted successfully", deleted_project
