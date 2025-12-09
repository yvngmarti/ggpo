from sqlalchemy.orm import Session
from app.models import Role
from app.api.schemas.role_schema import CreateRoleSchema, UpdateRoleSchema


def get_roles(db: Session):
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, role_name: str):
    return db.query(Role).filter(Role.name == role_name).first()


def create_role(db: Session, create_role_schema: CreateRoleSchema):
    db_role = Role(
        name=create_role_schema.name,
        description=create_role_schema.description,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, update_role_schema: UpdateRoleSchema):
    db_role = db.query(Role).filter(Role.id == role_id).first()

    update_data = update_role_schema.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_role, field, value)

    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    db.delete(db_role)
    db.commit()
    return db_role
