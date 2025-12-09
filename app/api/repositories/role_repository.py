from sqlalchemy.orm import Session
from app.models import Role


class RoleRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Role).all()

    @staticmethod
    def get_by_id(db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def get_by_name(db: Session, role_name: str):
        return db.query(Role).filter(Role.name == role_name).first()

    @staticmethod
    def create(db: Session, role: Role):
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def update(db: Session, role: Role):
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def delete(db: Session, role: Role):
        db.delete(role)
        db.commit()
        return role
