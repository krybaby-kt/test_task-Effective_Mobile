from pydantic import BaseModel, Field


class UserPanelResponse(BaseModel):
    """Модель ответа для панели пользователя"""
    success: bool = Field(description="Успешность операции")
