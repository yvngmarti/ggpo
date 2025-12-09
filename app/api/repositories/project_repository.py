from sqlalchemy.orm import Session
from app.models import Project


class ProjectRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Project).all()

    @staticmethod
    def get_by_id(db: Session, project_id: int):
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_by_code(db: Session, project_code: str):
        return db.query(Project).filter(Project.code == project_code).first()

    @staticmethod
    def create(db: Session, project: Project):
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def update(db: Session, project: Project):
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(db: Session, project: Project):
        db.delete(project)
        db.commit()
        return project
