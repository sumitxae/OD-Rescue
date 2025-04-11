from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship
from ..models.base import AbstractBase
from ..enums.table_name_enums import TableNames
from sqlalchemy import Enum as SQLAlchemyEnum
from app.enums.role_enums import Roles

class Role(AbstractBase):
    __tablename__ = TableNames.ROLE.value

    role_id = Column(Integer, primary_key=True, index=True)
    role_type = Column(SQLAlchemyEnum(Roles, name="role_types"), nullable=False)
    is_active = Column(Boolean, default=True)
    permissions = Column(JSON, nullable=False)

    users = relationship("User", back_populates="role")