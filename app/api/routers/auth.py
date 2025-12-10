from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services import AuthService
from app.core.security import SecurityUtils
from app.api.schemas.auth_schema import TokenSchema
from app.api.helpers import get_auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    user = service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = SecurityUtils.create_access_token(subject=user.id)
    new_refresh_token = SecurityUtils.create_refresh_token(subject=user.id)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(
    refresh_token_str: str, service: AuthService = Depends(get_auth_service)
):
    new_access_token = service.refresh_access_token(refresh_token_str)
    return {"access_token": new_access_token, "token_type": "bearer"}
