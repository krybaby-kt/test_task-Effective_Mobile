from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class SignUpRequest(BaseModel):
    """Модель запроса для регистрации пользователя"""
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(description="Пароль пользователя", min_length=8, max_length=100)


class SignUpResponse(BaseModel):
    """Модель ответа для регистрации пользователя"""
    success: bool = Field(description="Успешность операции")


class SignInRequest(BaseModel):
    """Модель запроса для входа в систему"""
    email: Optional[EmailStr] = Field(description="Email пользователя", default=None)
    password: str = Field(description="Пароль пользователя", min_length=8, max_length=100)


class SignInResponse(BaseModel):
    """Модель ответа для входа в систему"""
    success: bool = Field(description="Успешность операции")


class SignOutResponse(BaseModel):
    """Модель ответа для выхода из системы"""
    success: bool = Field(description="Успешность операции")


class ChangePasswordRequest(BaseModel):
    """Модель запроса для смены пароля"""
    old_password: str = Field(description="Старый пароль пользователя", min_length=8, max_length=100)
    new_password: str = Field(description="Новый пароль пользователя", min_length=8, max_length=100)


class ChangePasswordResponse(BaseModel):
    """Модель ответа для смены пароля"""
    success: bool = Field(description="Успешность операции")
