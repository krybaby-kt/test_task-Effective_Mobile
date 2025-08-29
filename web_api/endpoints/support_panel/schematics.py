from pydantic import BaseModel, Field


class SupportPanelResponse(BaseModel):
    """Модель ответа для панели поддержки"""
    success: bool = Field(description="Успешность операции")
