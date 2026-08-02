from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import (
    UserCreate, UserResponse, Token,
    ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest,
)
from app.services.auth_service import AuthService
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user_data)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    from app.schemas.user import UserLogin

    service = AuthService(db)
    access_token = service.login(
        UserLogin(email=form_data.username, password=form_data.password)
    )
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.forgot_password(payload.email)
    return ForgotPasswordResponse(
        message="A password reset link has been generated.",
        reset_token=token,
    )


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    service.reset_password(payload.token, payload.new_password)
    return {"message": "Password has been reset successfully. You can now log in."}
