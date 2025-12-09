from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.services.role_service import RoleService
from fastapi import Depends


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)
