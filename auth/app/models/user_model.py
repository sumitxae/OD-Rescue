from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..models.base import AbstractBase
from app.enums.table_name_enums import TableNames
from .role_model import Role


class User(AbstractBase):
    __tablename__ = TableNames.USER.value

    user_id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)     
    is_user_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    
    role_id = Column(BigInteger, ForeignKey("roles.role_id"), nullable=True)
    role = relationship("Role", back_populates="users")

    
