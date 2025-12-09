from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.services import roles_service
from app.api.schemas import role_schema

# from src.api.helpers.response_wrapper import APIResponse
router = APIRouter(prefix="/roles", tags=["Roles"])
