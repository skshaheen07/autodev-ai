import secrets
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.core.security import verify_password, hash_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate):
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )
        user = self.user_repo.create(user_data)
        return user

    def login(self, credentials: UserLogin):
        user = self.user_repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return access_token

    def forgot_password(self, email: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No account found with this email.",
            )
        token = secrets.token_urlsafe(32)
        self.user_repo.set_reset_token(user, token)
        return token

    def reset_password(self, token: str, new_password: str) -> None:
        user = self.user_repo.get_by_reset_token(token)
        if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This reset link is invalid or has expired.",
            )
        self.user_repo.reset_password(user, hash_password(new_password))
