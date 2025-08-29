from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.roles import RoleModel
from database.models.rules import RuleModel


class RoleRuleModel(Base):
    __tablename__ = "role_rules"
    id = Column(BigInteger, unique=True, primary_key=True)
    
    role_name = Column(String, ForeignKey(RoleModel.name))
    rule_name = Column(String, ForeignKey(RuleModel.name))
    
    creating_date = Column(DateTime, default=datetime.datetime.now)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"