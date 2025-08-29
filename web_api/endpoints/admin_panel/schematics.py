from pydantic import BaseModel, Field
from typing import List


class AdminPanelResponse(BaseModel):
    """Модель ответа для панели администратора"""
    success: bool = Field(description="Успешность операции")


class RoleRuleItem(BaseModel):
    """Модель элемента роли с правилами"""
    role: str = Field(description="Название роли")
    rules: List[str] = Field(description="Список правил для роли")


class RolesAndRulesResponse(BaseModel):
    """Модель ответа со списком ролей и правил"""
    success: bool = Field(description="Успешность операции")
    content: List[RoleRuleItem] = Field(description="Список ролей с правилами")


class CreateRoleRequest(BaseModel):
    """Модель запроса создания роли"""
    name: str = Field(description="Название роли")
    comment: str = Field(description="Комментарий к роли")


class CreateRoleResponse(BaseModel):
    """Модель ответа создания роли"""
    success: bool = Field(description="Успешность операции")


class CreateRuleRequest(BaseModel):
    """Модель запроса создания правила"""
    name: str = Field(description="Название правила")
    comment: str = Field(description="Комментарий к правилу")


class CreateRuleResponse(BaseModel):
    """Модель ответа создания правила"""
    success: bool = Field(description="Успешность операции")


class CreateRoleRuleRequest(BaseModel):
    """Модель запроса создания связи между ролью и правилом"""
    role_name: str = Field(description="Название роли")
    rule_name: str = Field(description="Название правила")


class CreateRoleRuleResponse(BaseModel):
    """Модель ответа создания связи между ролью и правилом"""
    success: bool = Field(description="Успешность операции")


class DeleteRoleRequest(BaseModel):
    """Модель запроса удаления роли"""
    name: str = Field(description="Название роли")


class DeleteRoleResponse(BaseModel):
    """Модель ответа удаления роли"""
    success: bool = Field(description="Успешность операции")


class DeleteRuleRequest(BaseModel):
    """Модель запроса удаления правила"""
    name: str = Field(description="Название правила")


class DeleteRuleResponse(BaseModel):
    """Модель ответа удаления правила"""
    success: bool = Field(description="Успешность операции")


class DeleteRoleRuleRequest(BaseModel):
    """Модель запроса удаления связи между ролью и правилом"""
    role_name: str = Field(description="Название роли")
    rule_name: str = Field(description="Название правила")


class DeleteRoleRuleResponse(BaseModel):
    """Модель ответа удаления связи между ролью и правилом"""
    success: bool = Field(description="Успешность операции")


class RuleItem(BaseModel):
    """Модель элемента правила"""
    name: str = Field(description="Название правила")
    comment: str = Field(description="Комментарий к правилу")


class RulesResponse(BaseModel):
    """Модель ответа со списком правил"""
    success: bool = Field(description="Успешность операции")
    content: List[RuleItem] = Field(description="Список правил")


class RoleItem(BaseModel):
    """Модель элемента роли"""
    name: str = Field(description="Название роли")
    comment: str = Field(description="Комментарий к роли")


class RolesResponse(BaseModel):
    """Модель ответа со списком ролей"""
    success: bool = Field(description="Успешность операции")
    content: List[RoleItem] = Field(description="Список ролей")