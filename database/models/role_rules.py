"""
Модель связи между ролями и правами (связь Many-to-Many).
"""
from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.roles import RoleModel
from database.models.rules import RuleModel


class RoleRuleModel(Base):
    """
    Модель для хранения связей между ролями и правилами.
    
    Реализует отношение Many-to-Many между ролями и правами,
    позволяя одной роли иметь множество прав и одному праву
    принадлежать нескольким ролям.
    
    Attributes:
        id: Уникальный идентификатор связи
        role_name: Имя роли (внешний ключ на roles.name)
        rule_name: Имя правила (внешний ключ на rules.name)
        creating_date: Дата создания связи
    """
    __tablename__ = "role_rules"
    
    # Первичный ключ
    id = Column(BigInteger, unique=True, primary_key=True)
    
    # Ссылки на роль и правило
    role_name = Column(String, ForeignKey(RoleModel.name), nullable=False)
    rule_name = Column(String, ForeignKey(RuleModel.name), nullable=False)
    
    # Метаданные
    creating_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"