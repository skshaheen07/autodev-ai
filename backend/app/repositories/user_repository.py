from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_reset_token(self, token: str) -> User | None:
        return self.db.query(User).filter(User.reset_token == token).first()

    def create(self, user_data: UserCreate) -> User:
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_reset_token(self, user: User, token: str, expires_minutes: int = 30) -> None:
        user.reset_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(minutes=expires_minutes)
        self.db.commit()

    def reset_password(self, user: User, new_hashed_password: str) -> None:
        user.hashed_password = new_hashed_password
        user.reset_token = None
        user.reset_token_expires = None
        self.db.commit()
