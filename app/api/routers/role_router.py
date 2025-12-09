from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.services import role_service
from app.api.schemas import role_schema
from app.api.helpers.api_response import APIResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=APIResponse)
def get_roles(db: Session = Depends(get_db)):
    db_roles = role_service.get_roles(db)
    data = [role_schema.RoleResponseSchema.model_validate(rt) for rt in db_roles]
    message = "Roles retrieved successfully" if data else "No roles found"
    return APIResponse(status=True, message=message, data=data)
