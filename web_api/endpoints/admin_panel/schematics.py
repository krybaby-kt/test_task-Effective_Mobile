from pydantic import BaseModel, Field


class AdminPanelResponse(BaseModel):
    """Модель ответа для панели администратора"""
    success: bool = Field(description="Успешность операции")
