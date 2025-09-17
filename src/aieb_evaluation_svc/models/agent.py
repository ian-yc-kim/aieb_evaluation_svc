import datetime
import uuid

from sqlalchemy import Column, DateTime, String, UUID

from .base import Base


class Agent(Base):
    __tablename__ = 'agent'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
