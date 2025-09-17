import datetime
import uuid

from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint, UUID
)

from .base import Base


class EvaluationCriteria(Base):
    __tablename__ = 'evaluation_criteria'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey('agent.id'), nullable=False)
    version = Column(Integer, nullable=False)
    criteria_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    __table_args__ = (UniqueConstraint('agent_id', 'version', name='_agent_version_uc'),)
