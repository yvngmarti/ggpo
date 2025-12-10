from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.api.repositories.user_repository import UserRepository
from app.core.security import SecurityUtils
from app.core.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository()

    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(self.db, email)
        if not user:
            return None
        if not SecurityUtils.verify_password(password, user.password):
            return None
        return user

    def refresh_access_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")

            if not user_id or token_type != "refresh":
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            access_token = SecurityUtils.create_access_token(subject=user_id)
            return access_token
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            ) from exc
