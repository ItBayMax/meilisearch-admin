"""
Project model - represents a Meilisearch instance
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from .database import Base


class Project(Base):
    """Project model for storing Meilisearch instance information"""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, comment="Project name")
    url = Column(String(500), nullable=False, comment="Meilisearch instance URL")
    api_key = Column(String(500), nullable=True, comment="Master API key")
    description = Column(Text, nullable=True, comment="Project description")
    is_active = Column(Boolean, default=True, comment="Whether the project is active")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Creation time")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="Update time")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "api_key": self.api_key,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"
