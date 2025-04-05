from app.config.connect_db import Base
from sqlalchemy import Column, DateTime, String, Boolean
from datetime import datetime as dt

class AbstractBase(Base):
    __abstract__ = True
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.now(), nullable=False)
    updated_at = Column(DateTime, default=dt.now(), onupdate=dt.now(), nullable=False)