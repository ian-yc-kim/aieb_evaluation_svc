import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, JSON, UUID

from .base import Base


class Evaluation(Base):
    __tablename__ = 'evaluation'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    criteria_id = Column(UUID(as_uuid=True), ForeignKey('evaluation_criteria.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')
    agent_prompt = Column(Text, nullable=False)
    agent_output = Column(Text, nullable=True)
    results = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
